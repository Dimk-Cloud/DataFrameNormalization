import pandas as pd
from pandas import Series, DataFrame
from collections.abc import Iterable, Mapping
from functools import singledispatch

def get_nality(df: DataFrame) -> Series:
    '''Return data cardinality for each column of df'''

    return df.apply(lambda s : s.nunique(dropna=False) / s.size)
        

def df_normalize(df: DataFrame,
                 primary_name: str,
                 headers: int | float | Iterable[int] | Iterable[str] \
                 | Mapping[int, int | float] | Mapping[str, int | float]
                 ) -> dict[str, Series | DataFrame] | None:                              
    """Normalize the "df" DataFrame into a series of related tables
    with RDBMS-style relations.

    Returns the related tables as a dictionary:
    { 'table_name' : table as a Series or DataFrame, ... }
    The original table is a DataFrame, the newly created tables are Series.
    If the original table is not normalized, returns None

    primary_name: the name of the table the original normalized DataFrame
    is saved as. Other tables assume the names of df's columns
    that get normalized.

    The 'headers' keyword argument defines the original DataFrame's columns to
    be normalized and is interpreted as follows:

    int | float: Cardinality Threshold (CT), which applies across all columns
    and lies in the range of [0, 1]. If the share of unique values in a column, 
    i.e. the number of unique values in proportion to the column's length,
    does not exceeds this value, the column will be normalized.
    CT = 0 | 1: The column will not be | will be normalized.
    
    Iterable[int] | Iterable[str]:
    Zero-based column numbers | column names to be normalized,
    without regard to the CT.

    Mapping[int, int | float] | Mapping[str, int | float]: provides a mapping of
    { zero-based column number | column name : CT }, i.e., the CT value for each
    provided column.
    """

    # Checking the input parameters' types
    #
    if not isinstance(df, DataFrame):
        raise TypeError('df must be a pandas DataFrame')

    if not isinstance(primary_name, str):
        raise TypeError('primary_name must be a string')

    # Defining the list of columns up for normalization, with singledispatch
    #
    @singledispatch         # The generic's function entry point
    def get_norm_headers(headers: object) -> None:  
        raise ValueError('headers must be an integer, float, Mapping or Iterable')

    @get_norm_headers.register  # If a single CT is provided for all columns
    def _(headers: int | float) -> list:

        if headers < 0 or headers > 1:
            raise ValueError('headers must be in the closed interval of [0, 1]')

        return [header for header, series in df.items()
                 if (series.nunique(dropna=False) / len(series)) <= headers]
        

    @get_norm_headers.register
    def _(headers: Iterable) -> list | pd.Index:

        normheads: int | str = list(headers)

        # If it's an Iterable of ints
        if all(isinstance(header, int) for header in normheads):
            return df.columns.take(normheads)

        # If it's an Iterable of strings
        elif all(isinstance(header, str) for header in normheads):
            return normheads

        else:
            raise ValueError('If Iterable, headers should be Iterable[int] | Iterable[str]')
        
    
    @get_norm_headers.register
    def _(headers: Mapping) -> pd.Index:

        normheads: int | str = list(headers.keys())

        # If it's a Mapping of {column number : CT}
        if all(isinstance(header, int) and isinstance(ct, (int, float))
               for header, ct in headers.items()
               ):

            return [header for headnum, (header, series) in enumerate(df.items())
                    if (headnum in normheads) and
                    series.nunique(dropna=False) / len(series) <= headers[headnum]]
        
        # If it's a Mapping of {column name : CT}
        elif all(isinstance(header, str) and isinstance(ct, (int, float))
                  for header, ct in headers.items()
                 ):

            return [header for header, series in df.items()
                    if (header in normheads) and
                    series.nunique(dropna=False) / len(series) <= headers[header]]

        else:
            raise ValueError('If Mapping, headers should be either '
                             '{int : int | float} or {str : int | float}')

    # The dictionary { "normalized_table_name" : DataFrame }
    # containing the returned normalized tables 
    result_tables = dict()

    if not (headers_to_normalize := get_norm_headers(headers)):
        return None

    # The original table, saved as "primary_name"
    result_tables[primary_name] = df.copy()


    for header in headers_to_normalize:
        distinct_items = df[header].drop_duplicates(ignore_index=True)
        result_tables[header] = distinct_items
        result_tables[primary_name][header] = (result_tables[primary_name][header]
                                               .map(Series(data = distinct_items.index,
                                                           index = distinct_items.values)
                                                   )
                                               )
    return result_tables
    
    





