# author: Anthea Chen
# date: 2021-11-24

"""Get corresponding country code for train_df

Usage: get_countrycode_data.py --path=<path> --out_file=<out_file> 
 
Options:
--path=<path>             the data to process
--out_file=<out_file>   Path (including filename) of where to locally write the file
"""

import pycountry
import pandas as pd
from docopt import docopt
import os

opt = docopt(__doc__)

def main(path, out_file):
    df = pd.read_csv(path)
    CODE=[]
    for country in df.Country:
        try:
            code=pycountry.countries.get(name=country).alpha_3
            CODE.append(code)
        except:
            CODE.append('None')
            
    # create a column for code 
    df['code']=CODE
    replace_dict = {
    "South Korea":"KOR",
    "Souh Korea":"KOR",
    "Taiwan":"CHN",
    "Vietnam":"VNM",
    "UK":"GBR",
    "Russia":"RUS",
    "Holland":"NLD",
    "Sarawak":"MYS",
    "Dubai":"ARE",
    "USA":"USA"}

    for key,value in replace_dict.items():
        df.loc[df["Country"] == key, "code"] = value

    #save the file
    try:
        df.to_csv(out_file, index = False)
    except:
        os.makedirs(os.path.dirname(out_file))
        df.to_csv(out_file, index = False)
if __name__ == "__main__":
    main(opt["--path"], opt["--out_file"])
