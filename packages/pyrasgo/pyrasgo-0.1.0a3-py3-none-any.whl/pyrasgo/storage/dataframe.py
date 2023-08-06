import pandas as pd
from typing import List, Optional

from pyrasgo.api.error import APIError
from pyrasgo.utils import naming


def build_schema(df: pd.DataFrame, include_index=False) -> dict:
    from pandas.io.json import build_table_schema
    schema_list = build_table_schema(df)
    if not include_index:
        return {column['name']: column
                for column in schema_list['fields'] if column['name'] != 'index'}
    return {column['name']: column
            for column in schema_list['fields']}


def generate_ddl(df: pd.DataFrame,
                 table_name: str,
                 append: Optional[bool] = False):
    #default is overwrite
    create_statement = "CREATE TABLE IF NOT EXISTS" if append else "CREATE OR REPLACE TABLE"
    return pd.io.sql.get_schema(df, table_name) \
        .replace("CREATE TABLE", create_statement) \
        .replace('"', '')

def confirm_df_columns(df: pd.DataFrame, dimensions: List[str], features: List[str]):
    confirm_list_columns(list(df.columns), dimensions, features)

def confirm_list_columns(columns: list, dimensions: List[str], features: List[str]):
    missing_dims = []
    missing_features = []
    consider = []
    for dim in dimensions:
        if dim not in columns:
            missing_dims.append(dim)
            if naming._snowflakify_name(dim) in columns:
                consider.append(naming._snowflakify_name(dim))
    for ft in features:
        if ft not in columns:
            missing_features.append(ft)
            if naming._snowflakify_name(ft) in columns:
                consider.append(naming._snowflakify_name(ft))
    if missing_dims or missing_features:
        raise APIError(f"Specified columns do not exist in dataframe: "
                        f"Dimensions({missing_dims}) Features({missing_features}) "
                        f"Consider these: ({consider})?")

def quality_scan(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """ 
    Preform all data quality scans 
    
    Find missing data
    Find duplicates
    
    Returns 2 dataframes
    """
    return find_missing_data(df), find_duplicate_rows(df)

def find_type_mismatches(df: pd.DataFrame, column: str, data_type: str) -> pd.DataFrame:
    """ 
    Return a copy of your DataFrame with a column cast to another datatype
    
    df: pandas DataFrame
    column: The column name in the DataFrame to cast
    data_type: the data type to cast to Accepted Values: ['datetime', 'numeric']
    """
    new_df = pd.DataFrame()
    if data_type == 'datetime':
        new_df[column] = pd.to_datetime(df[column], errors='coerce', infer_datetime_format=True)
    elif data_type == 'numeric':
         new_df[column] = pd.to_numeric(df[column], errors='coerce')
    else:
        return "Supported data_type values are: 'datetime' or 'numeric'"
    total = df[column].count()
    cant_convert = new_df[column].isnull().sum()
    print(f"{(total - cant_convert) / total}%: {cant_convert} rows of {total} rows cannot convert.")
    new_df.rename(columns = {column:f'{column}CastTo{data_type.title()}'}, inplace = True)
    return new_df

def find_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Print all columns in a Dataframe with null values
    and return rows with null values
    
    Response:   Columns with null values:
                -------------------------
                column, count of rows
                -------------------------
                List[index of rows with null values]
    
    df: pandas DataFrame
    """
    column_with_nan = df.columns[df.isnull().any()]
    template="%-20s %-6s"
    print(template % ("Column", "Count of Nulls"))
    print("-"*35)
    for column in column_with_nan:
        print(template % (column, df[column].isnull().sum()))
    print("-"*35)
    return df[df.isnull().any(axis=1)]

def remove_rows_with_missing_data(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """
    Returns a copy of your DataFrame after removing all rows 
    containing NULL or NaN values in any of their columns
    
    df: pandas DataFrame
    columns: (Optional) List of column names to check for nulls, Defaults to All
    """
    df_out = df.copy(deep=True)
    if columns:
        index_with_nan = pd.Int64Index([])
        for column in columns:
            index_with_nan = index_with_nan.append(df_out[df_out[column].isnull()].index)
    else:
        index_with_nan = df_out.index[df_out.isnull().any(axis=1)]
    print(f'Dropping {index_with_nan.shape[0]} rows')
    df_out = pd.DataFrame(df_out.drop(index_with_nan))
    return df_out

def remove_columns_with_missing_data(df: pd.DataFrame, columns: List[str] = None, threshold: float = 0) -> pd.DataFrame:
    """
    Returns a copy of your dataframe after removing columns 
    containing NULL or NaN values exceeding a threshold count
    
    df: pandas DataFrame
    columns: (Optional) List of column names to check for null, Defaults to All
    threshold: (Optional) null percentage threshold above which a column will be dropped, Defaults to 0%
    """
    df_out = df.copy(deep=True)
    column_with_nan = df_out.columns[df_out.isnull().any()]
    for column in column_with_nan:
        if columns:
            if column in columns:
                if df_out[column].isnull().sum()*100.0/df_out.shape[0] >= threshold:
                    df_out = df_out.drop(column, 1)
                    print(f'Column deleted: {column}')
        else:
            if df_out[column].isnull().sum()*100.0/df_out.shape[0] >= threshold:
                df_out = df_out.drop(column, 1)
                print(f'Column deleted: {column}')
    return df_out

def find_duplicate_rows(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """ 
    Returns a DataFrame of rows that are duplicated in your original DataFrame 
    
    df: pandas DataFrame
    columns: (Optional) List of column names to check for duplicates in
    """
    df_out = df.copy(deep=True)
    if columns:
        df_out = df.iloc[:0].copy()
        for column in columns:
            df_out = df_out.append(df[df.duplicated([column])])
    else:
        df_out = df[df.duplicated()]
    return df_out

def remove_duplicate_rows(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """ 
    Returns a copy of your DataFrame with duplicate rows removed

    df: pandas DataFrame
    columns: (Optional) List of column names to check for duplicates in
    """
    df_out = df.copy(deep=True)
    #df_out = df_out.reset_index(drop=False)
    #df_out.rename(columns = {'index':'indexInOrigDF'}, inplace = True)
    if columns:
        drop_us = pd.Int64Index([])
        for column in columns:
            drop_us = drop_us.append(df_out[df_out.duplicated([column])].index)
    else:
        drop_us = df_out.index[df_out.duplicated()]
    print(f'Dropping {drop_us.shape[0]} rows')
    df_out = pd.DataFrame(df_out.drop(drop_us, 0))
    return df_out

def scan_for_timeseries_gaps(df: pd.DataFrame, column: str):
    # Return rows before and after timeseries gaps 
    pass

def _snowflakify_dataframe(df: pd.DataFrame):
    """
    Renames all columns in a pandas dataframe to Snowflake compliant names in place
    """
    df.rename(columns={r: naming._snowflakify_name(r) for r in build_schema(df)},
                inplace=True)