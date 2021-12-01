# author: Anthea Chen
# date: 2021-11-19

"""Split the downloaded dataframe into train and test sets

Usage: split.py --path=<path> --out_file_train=<out_file_train> --out_file_test=<out_file_test>
 
Options:
--path=<path>                       The train dataframe to split
--out_file_train=<out_file_train>   Path (including filename) of where to locally write the train data
--out_file_test=<out_file_test>     Path (including filename) of where to locally write the test data
"""

from docopt import docopt
import pandas as pd
from sklearn.model_selection import train_test_split
import os

opt = docopt(__doc__)

def main(path, out_file_train, out_file_test):
    # Read the df
    df = pd.read_csv(path)

    # Split the data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)

    # Save the train data as csv
    try:
        train_df.to_csv(out_file_train, index = False)
    except:
        os.makedirs(os.path.dirname(out_file_train))
        train_df.to_csv(out_file_train, index = False)

    # Save the test data as csv
    try:
        test_df.to_csv(out_file_test, index = False)
    except:
        os.makedirs(os.path.dirname(out_file_test))
        test_df.to_csv(out_file_test, index = False)

if __name__ == "__main__":
    main(opt["--path"], opt["--out_file_train"], opt["--out_file_test"])
