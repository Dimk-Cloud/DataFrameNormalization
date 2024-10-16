import pandas as pd
import numpy as np
import random

from pandas import DataFrame
from pprint import pp

from dfnorm import df_normalize

# Setting comfortable display options
# -----------------------------------
pd.set_option("display.max_columns", 13)
pd.set_option("display.width", 400)
pd.set_option("display.max_rows", 80)
#pd.set_option("display.max_colwidth", 30)

DF_NAME = r'<path to a *.csv file>'

df = pd.read_csv(DF_FNAME)

# Tests
# -----

nality_name = {name : series.nunique()/len(series) for name, series in df.items()}

nality_ord = {colnum : series.nunique()/len(series)
               for colnum, (_, series) in enumerate(df.items(), 1)}

cnum = {colname : i for i, colname in enumerate(df.columns, 1)}

# Cardinality threshold (OK)
'''

for ct in np.linspace(0, 1, 6):
    print(f'{ct = }')
    pp(df_normalize(df, '_', ct))
'''

# Zero-based column numbers to be normalized (Iterable[int]) (OK)
'''
# number of trials
RUNS = 100  
# map column names to positional numbers

for _ in range(RUNS):
    # a list of random header numbers
    headers = random.sample(range(0, len(df.columns)),
                            random.randrange(1, len(df.columns)+1)
                            )
    
    assert sorted(headers) == sorted(list(df_normalize(df, '_', headers).map(cnum)))
'''    

# Column names to be normalized (Iterable[str]) (OK)
'''
# number of trials
RUNS = 100  

for _ in range(RUNS):
    # a list of random column names
    headers = random.sample(df.columns.to_list(),
                            random.randrange(1, len(df.columns)+1)
                            )
    assert headers == df_normalize(df, '_', headers)
'''
         
# A Mapping of {column number : CT} (OK)
'''
RUNS = 100

for _ in range(RUNS):
    headers = {colnum : random.choice(np.linspace(0, 1, 6))
               for colnum in random.sample(range(0, len(df.columns)),
                                           random.randrange(1, len(df.columns)+1))}

    headers_to_norm = [colnum + 1 for colnum, ct in headers.items() if nality_ord[colnum+1] <= ct]
    assert sorted(list(map(lambda colnum : cnum[colnum], df_normalize(df, '_', headers)))) == sorted(headers_to_norm)
'''    

# A Mapping of {column name : CT}
'''    
RUNS = 100

for _ in range(RUNS):
    headers = {colname : random.choice(np.linspace(0, 1, 6))
               for colname in random.sample(list(df.columns), random.randrange(len(df.columns)))}
    
    headers_to_norm = [colname for colname, ct in headers.items() if nality_name[colname] <= ct]
    assert sorted(list(df_normalize(df, '_', headers))) == sorted(headers_to_norm)
'''    


