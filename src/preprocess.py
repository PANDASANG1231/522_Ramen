# author: Anthea Chen
# date: 2021-11-25

"""preprocess for dataframe

Usage: preprocess.py --train_path=<train_path> --test_path=<test_path> --out_file_train=<out_file_train> --out_file_test=<out_file_test>  
 
Options:
--train_path=<train_path>             the train dataframe to process
--test_path=<test_path>               the test dataframe to process
--out_file_train=<out_file_train>   Path (including filename) of where to locally write the train data
--out_file_test=<out_file_test>     Path (including filename) of where to locally write the test data
"""

import pycountry
from docopt import docopt
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import os

opt = docopt(__doc__)

def main(train_path, test_path, out_file_train, out_file_test):
    # Read two df
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    # Relevant transform
    categorical_features = ["Brand", "Style", "Country"]
    drop_features = ["Review","Variety", "Top Ten"]
    target = ["Stars"]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore",sparse=False)

    preprocessor = make_column_transformer(
     (categorical_transformer, categorical_features)
    )
    train_trans = preprocessor.fit_transform(df_train)
    test_trans = preprocessor.transform(df_test)

    # Get the transformed data 
    train_out = pd.DataFrame(
      data=train_trans,
      columns=preprocessor.get_feature_names_out(),
      index=df_train.index,
    )
    train_out["Stars"] = df_train["Stars"]

    test_out = pd.DataFrame(
      data=test_trans,
      columns=preprocessor.get_feature_names_out(),
      index=df_test.index,
    )
    test_out["Stars"] = df_test["Stars"]

    # Save the train data as csv
    try:
        train_out.to_csv(out_file_train, index = False)
    except:
        os.makedirs(os.path.dirname(out_file_train))
        train_out.to_csv(out_file_train, index = False)

    # Save the test data as csv
    try:
        test_out.to_csv(out_file_test, index = False)
    except:
        os.makedirs(os.path.dirname(out_file_test))
        test_out.to_csv(out_file_test, index = False)

if __name__ == "__main__":
    main(opt["--train_path"], opt["--test_path"], opt["--out_file_train"], opt["--out_file_test"])
