"""
Usage: src/train_model.py --in_file=<in_file> --out_model_file=<out_model_file>
Options:
--in_file=<in_file>                  Path of where to locally read the file
--out_model_file=<out_model_file>    Path of where to locally write the model

Acknowledgement:
This script is copied and adapted from https://github.com/ttimbers/breast_cancer_predictor/blob/master/src/download_data.py
"""
  
from docopt import docopt

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

    
def main(in_file, out_model_file):
    
    print(in_file, out_model_file)
    
    
if __name__ == "__main__":
    main(opt["--in_file"], opt["--out_model_file"])

