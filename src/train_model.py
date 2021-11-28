# date: 2021-11-25

"""Train the model

Usage: train_model.py --train_file=<train_file> --out_file_train=<out_file_train> 
 
Options:
--train_file=<train_file>           the train dataframe to train
--out_file_train=<out_file_train>   Path (including filename) of where to locally write the model
"""

from docopt import docopt
from tool.tool_function import *

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.feature_selection import RFE, RFECV


from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    average_precision_score, 
)


opt = docopt(__doc__)

def main(train_file, out_file_train):
    
    
    train_data = pd.read_csv(train_file)
    train_data["Stars"] = train_data["Stars"].replace("Unrated", -1).astype(float).apply(handle_target)

    list_feature = [x for x in train_data if x != "Stars"]

    X_train, y_train = train_data[list_feature], train_data["Stars"]

    pipe_rfe_ridgecv = make_pipeline(RFE(Ridge()), LogisticRegression())
    pipe_rfe_ridgecv.fit(X_train, y_train)


    print("Plotting metrics in './../results/train_metrics.jpg' ...")
    evaluate_performance(y_train, pipe_rfe_ridgecv.predict_proba(X_train)[:, 1], save="./../results/train_metrics.jpg")
    new_columns = pipe_rfe_ridgecv[0].get_feature_names_out()
    coef_df = pd.DataFrame({"coef": pipe_rfe_ridgecv[-1].coef_[0], "vars": new_columns})
    coef_df["coef_abs"] = abs(coef_df["coef"])
    print("Like variables")
    coef_df.sort_values("coef", ascending=False).head(20).to_csv("./../results/Top_20_Good_features.csv", index=False)
    print("Hate variables")
    coef_df.sort_values("coef", ascending=True).head(20).to_csv("./../results/Top_20_Bad_features.csv", index=False)

    print(f"Writing model in '{out_file_train}' ...")
    pickle.dump(pipe_rfe_ridgecv, open(out_file_train, "wb"))
    
    
if __name__ == "__main__":
    main(opt["--train_file"], opt["--out_file_train"])

