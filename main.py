import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pprint import pp

import dfnorm

# Setting comfortable display options
# -----------------------------------
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)
#pd.set_option("display.max_colwidth", 30)

DF_NAME = r'<path to a *.csv file>'

# import the CSV file into a DataFrame
#df = pd.read_csv(DF_NAME)

# or a pickle
#df = pd.read_pickle(r'<path to a *.pkl file')

r = result = dfnorm.df_normalize(df,
                                 primary_name = 'main',
                                 headers = 0.5)
