# date: 2021-11-25

"""Predict

Usage: predict.py --test_file=<test_file> --model_file=<model_file>  [--target_name=<target_name>]
 
Options:
--test_file=<test_file>           the test dataframe to predict
--model_file=<model_file>   Path (including filename) of the model
[--target_name=<target_name>]   if test_file has a target col, put the column name here

"""
import pickle
import numpy as np
import pandas as pd
from docopt import docopt
from tool.tool_function import *

opt = docopt(__doc__)
## Preprocess the target

def main(test_file, model_file, target_name=None):
    
    data = pd.read_csv(test_file)
    model = pickle.load(open(model_file, "rb"))
    
    data[target_name] = data[target_name].replace("Unrated", -1).astype(float).apply(handle_target)
    list_feature = [x for x in data if x != target_name]
    X_test, y_test = data[list_feature], data[target_name]

    data["Prediction"] = model.predict_proba(X_test)[:, 1]
    print("Writing prediction result in './../results/prediction/prediction.csv' ...")
    data.to_csv("./../results/prediction/prediction.csv", index=False)

    print("Plotting metrics in './../results/test_metrics.jpg' ...")
    if target_name is not None:
        evaluate_performance(y_test, model.predict_proba(X_test)[:, 1], save="./../results/test_metrics.jpg")
        
if __name__ == "__main__":
    print(opt["--target_name"])
    if len(opt["--target_name"]) > 0:
        main(opt["--test_file"], opt["--model_file"], opt["--target_name"])
    else:
        main(opt["--test_file"], opt["--model_file"])
