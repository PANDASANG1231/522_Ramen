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
from sklearn.metrics import ConfusionMatrixDisplay 


def gen_confusion_matrix(model, X_test, y_test, out_file_result):
    
    cm = ConfusionMatrixDisplay.from_estimator(
        model, X_test[model.feature_names_], y_test, values_format="d", display_labels=["Bad ramen", "Good ramen"]
    )
    
    plt.savefig(os.path.join(out_file_result, 'confusion_matrix.jpg'))
    
    
opt = docopt(__doc__)
## Preprocess the target

def main(test_file, model_file, out_file_result, target_name):
    
    model = pickle.load(open(model_file, "rb"))
    X_test, y_test = load_data(test_file)

    gen_confusion_matrix(model, X_test, y_test, out_file_result)

    X_test["Prediction"] = model.predict_proba(X_test)[:, 1]
    X_test["Label"] = y_test

    prediction_path = os.path.join(out_file_result, 'prediction.csv')
    print("Writing prediction result in '{}' ...".format(prediction_path))
    X_test.to_csv(prediction_path, index=False)

if __name__ == "__main__":
    
    main(opt["--test_file"], opt["--model_file"], opt["--out_file_result"], "Stars")
