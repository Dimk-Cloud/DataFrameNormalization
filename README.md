# Normalization of pandas DataFrames.

The normalization of a DataFrame here refers to the process of reducing data redundancy by moving repeated data points from the DataFrame to a set of separate tables, represented as Series. This is similar to what is done in a relational database. After the normalization is completed, references to the repeated data points are stored in the copy of the original DataFrame instead of the data itself.

The process is centered on the notion of cardinality: a ratio of the unique data points in a column to the column's length. The lower a column's cardinality, the more sense it makes to normalize it.

The `dfnorm` module contains two functions:


`def get_nality(df: DataFrame) -> Series`,

a helper function, which returns cardinality values of df's columns.


`def df_normalize(df: DataFrame,
                 primary_name: str,
                 headers: int | float | Iterable[int] | Iterable[str] \
                 | Mapping[int, int | float] | Mapping[str, int | float]
                 ) -> dict[str, Series | DataFrame] | None`,

which normalizes the df DataFrame. This function is flexible and allows to specify columns to normalize in many ways, including by providing a cardinality threshold for each column; if a column's cardinality does not exceed the threshold, the column will be normalized.

The function's \_\_doc\_\_ contains a detailed description of the functions' arguments.

The `main` module has a simple example of calling the function.

The `test` module contains some random tests of the function. 
