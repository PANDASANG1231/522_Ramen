# date: 2021-11-25

"""Predict

Usage: predict.py --test_file=<test_file> --model_file=<model_file> --out_file_result=<out_file_result> 
 
Options:
--test_file=<test_file>           the test dataframe to predict
--model_file=<model_file>   Path (including filename) of the model
--out_file_result=<out_file_result>   Path (including filename) of where to locally write the results
"""
import os
import pickle
import numpy as np
import pandas as pd
from docopt import docopt
from tool.tool_function import *

opt = docopt(__doc__)
## Preprocess the target

def main(test_file, model_file, out_file_result, target_name):
    
    data = pd.read_csv(test_file)
    model = pickle.load(open(model_file, "rb"))
    
    data[target_name] = data[target_name].replace("Unrated", -1).astype(float).apply(handle_target)
    list_feature = [x for x in data if x != target_name]
    X_test, y_test = data[list_feature], data[target_name]
    
    prediction_path = os.path.join(out_file_result, 'prediction/prediction.csv')
    test_metric_path = os.path.join(out_file_result, 'test_metrics.jpg')


    data["Prediction"] = model.predict_proba(X_test)[:, 1]
    print("Writing prediction result in '{}' ...".format(prediction_path))
    data.to_csv(prediction_path, index=False)

    print("Plotting metrics in '{}' ...".format(test_metric_path))
    evaluate_performance(y_test, model.predict_proba(X_test)[:, 1], save=test_metric_path)
        
if __name__ == "__main__":
    main(opt["--test_file"], opt["--model_file"], opt["--out_file_result"], "Stars")

