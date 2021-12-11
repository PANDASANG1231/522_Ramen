import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_validate
from sklearn.metrics import roc_curve, auc

def handle_target(x, thresh=3.5):
    
    if x < thresh:
        return 0
    else:
        return 1

def load_data(file):
    
    data = pd.read_csv(file)
    print(data.shape)
    data["Stars"] = pd.to_numeric(data["Stars"], errors='coerce').fillna(-1).astype(float).apply(handle_target)
    X, y = data.drop(["Stars"], axis=1), data["Stars"]
    
    return X, y


def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    
    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)


