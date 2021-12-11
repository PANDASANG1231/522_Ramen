# date: 2021-11-25

"""Train the model

Usage: train_model.py --train_file=<train_file> --out_file_train=<out_file_train> --out_file_result=<out_file_result>
 
Options:
--train_file=<train_file>           the train dataframe to train
--out_file_train=<out_file_train>   Path (including filename) of where to locally write the model
--out_file_result=<out_file_result>   Path (including filename) of where to locally write the results
"""

from docopt import docopt
from tool.tool_function import *

import os
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
from boruta import BorutaPy
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import cross_validate
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostClassifier

def load_data(file):
    
    data = pd.read_csv(file)
    print(data.shape)
    data["Stars"] = pd.to_numeric(data["Stars"], errors='coerce').fillna(-1).astype(float).apply(handle_target)
    X, y = data.drop(["Stars"], axis=1), data["Stars"]
    
    return X, y

def feature_selection(X_train, y_train):
    
    pipe_rfe_ridgecv = RFECV(Ridge(), cv=2)
    pipe_rfe_ridgecv.fit(X_train, y_train)

    forest = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
    feat_selector = BorutaPy(forest, n_estimators='auto', verbose=2, random_state=1, perc=90)
    feat_selector.fit(X_train.values, y_train)

    feature_ranks = pd.DataFrame([X_train.columns, feat_selector.ranking_, feat_selector.support_]).T
    feature_ranks.columns = ["feature", "rank", "keep"]
    feature_ranks["keep_ridge"] = feature_ranks.feature.apply(lambda x: True if x in pipe_rfe_ridgecv.get_feature_names_out() else False)
    feature_ranks = feature_ranks.sort_values("rank")
    feature_ranks

    features_1 = feature_ranks["feature"].to_list()
    features_2 = feature_ranks[feature_ranks["keep"] == True]["feature"].to_list()
    features_3 = feature_ranks[(feature_ranks["keep"] == True) | (feature_ranks.head(300)["keep_ridge"] == True)]["feature"].to_list()

    return features_1, features_2, features_3


def model_selection(models, feature_lists, X_train, y_train, out_file_result):

    rst_all = []

    for features_list in feature_lists:

        rst_df=[]
        for model in models:
            tmp_df=pd.DataFrame(mean_std_cross_val_scores(models[model], X_train[features_list], y_train,
                                                        return_train_score=True, cv=5), columns=[model+"_"+str(len(features_list))])
            rst_df.append(tmp_df)

        rst_df=pd.concat(rst_df, axis=1)
        
        rst_all.append(rst_df)


    rst_all = pd.concat(rst_all, axis=1).T

    col_name = ["CatBoost", "LR", "RF", "SVM"]

    rst_all_test = rst_all[["test_score"]].copy()
    rst_all_test.loc[:, "model"] = [x.split("_")[0] for x in rst_all_test.index]
    rst_all_test.loc[:, "var_num"] = [x.split("_")[1] for x in rst_all_test.index]
    rst_all_test.loc[:, "test_score"] = [float(x.split("(+")[0].strip()) for x in rst_all_test.test_score]
    rst_all_test = pd.crosstab(columns=rst_all_test["model"], index=rst_all_test["var_num"], values=rst_all_test["test_score"], aggfunc=sum)
    rst_all_test.columns = col_name

    rst_all_train = rst_all[["train_score"]].copy()
    rst_all_train.loc[:, "model"] = [x.split("_")[0] for x in rst_all_train.index]
    rst_all_train.loc[:, "var_num"] = [x.split("_")[1] for x in rst_all_train.index]
    rst_all_train.loc[:, "test_score"] = [float(x.split("(+")[0].strip()) for x in rst_all_train.train_score]
    rst_all_train = pd.crosstab(columns=rst_all_train["model"], index=rst_all_train["var_num"], values=rst_all_train["test_score"], aggfunc=sum)
    rst_all_train.columns = col_name

    fig, axs = plt.subplots(1, 2, figsize=(12,4))

    sns.heatmap(rst_all_test, cmap="YlGnBu", linewidths=.5, annot=True, fmt=".3f", ax=axs[0])
    axs[0].set_title("Valid acurracy of different combinations")
    sns.heatmap(rst_all_train - rst_all_test, cmap="YlGnBu", linewidths=.5, annot=True, fmt=".3f", ax=axs[1])
    axs[1].set_title("Train\Valid acurracy gap of different combinations")

    plt.tight_layout()
    plt.savefig(os.path.join(out_file_result, 'feature_model_selection.jpg'), dpi=1600)


def model_train(X_train, y_train, feature_list, out_file_result):
    
    from scipy.stats import randint

    param_grid = {
        "learning_rate": np.linspace(0.05,0.3,10),
        "max_depth": randint(3, 7),
        "n_estimators": [400, 500, 600, 700, 800],
    }
    model = CatBoostClassifier(random_state=123, verbose=0,class_weights=[0.2, 0.3])
    rscv = RandomizedSearchCV(model, param_grid, scoring='accuracy', cv=5, return_train_score=True)
    rscv.fit(X_train[feature_list], y_train)
    
    final_model = CatBoostClassifier(random_state=123, verbose=0,class_weights=[0.2, 0.3], **rscv.best_params_)
    
    scores = cross_validate(
        final_model, X_train[feature_list], y_train, return_train_score=True, scoring=["accuracy", "f1", "recall", "precision",]
    )
    df = pd.DataFrame(scores).iloc[:, 2:]
    df.index = ["fold_"+str(i) for i in df.index]
    df.columns = [i.replace("test", "valid") for i in df.columns]
    df.to_csv(os.path.join(out_file_result, 'cross_valid_metric.csv'), index=False)
    
    final_model.fit(X_train[feature_list], y_train)
    
    return final_model


opt = docopt(__doc__)

def main(train_file, out_file_train, out_file_result):
    
    X_train, y_train = load_data(train_file)
    print("##########")
    print("Start model_selection and feature selection")

    features_1, features_2, features_3 = feature_selection(X_train, y_train)
    feature_lists = [features_1, features_2, features_3]

    models={
        "LogisticRegression": LogisticRegression(random_state=123, class_weight='balanced'),
        "RandomForest": RandomForestClassifier(random_state=123, class_weight='balanced'),
        "SVC": SVC(random_state=123, class_weight='balanced'),
        "CatBoost": CatBoostClassifier(random_state=123, verbose=0,class_weights=[0.2, 0.3])
    }

    model_selection(models, feature_lists, X_train, y_train, out_file_result)
    
    print("##########")
    print("The result of model_selection and feature selection is: CatBoost and features_2.")
    print("Start model train")

    final_model = model_train(X_train, y_train, feature_list=features_2, out_file_result=out_file_result)

    print(f"Writing model in '{out_file_train}' ...")
    pickle.dump(final_model, open(out_file_train, "wb"))
    
    
if __name__ == "__main__":
    main(opt["--train_file"], opt["--out_file_train"], opt["--out_file_result"])

