# author: Anthea Chen
# date: 2021-11-25

"""preprocess for dataframe

Usage: preprocess.py --path=<path> --out_file=<out_file> 
 
Options:
--path=<path>             the data to process
--out_file=<out_file>   Path (including filename) of where to locally write the file
"""

import pycountry
from docopt import docopt
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import os

opt = docopt(__doc__)

def main(path, out_file):
    # Read the df
    df = pd.read_csv(path)

    # Relevant transform
    categorical_features = ["Brand", "Variety", "Style", "Country"]
    drop_features = ["Review","Top Ten"]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore",sparse=False)

    preprocessor = make_column_transformer(
     (categorical_transformer, categorical_features)
    )
    df_trans = preprocessor.fit_transform(df)

    # Get the transformed data 
    df_out = pd.DataFrame(
      data=df_trans,
      columns=preprocessor.get_feature_names_out(),
        index=df.index,
    )

    # Save the data as csv
    try:
        df_out.to_csv(out_file, index = False)
    except:
        os.makedirs(os.path.dirname(out_file))
        df_out.to_csv(out_file, index = False)
if __name__ == "__main__":
    main(opt["--path"], opt["--out_file"])
