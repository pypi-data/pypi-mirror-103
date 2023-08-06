#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
from jtlib import file_utils


TEMP_DIR = os.path.expanduser('~') + '.jtlib/temp/'
ENCODING = 'ISO-8859-1'


def read_data_to_df(filepath, remove_unnamed=False, header='infer', multiple_tables=False):
    """
    Helper function for reading data into a pandas DataFrame.

    Args:
        (str) filepath - path to file containing data to be read.
        (boolean) remove_unnamed - Set to True to ignore columns without a header. Defaults to False.
        (int, list of int) header - Row number to use as the column names. Default to 'infer' column headers.
        (boolean) multiple_tables - If there are multiple tables, a list will be returned. Defaults to False.
    
    Returns:
        df - pandas DataFrame containing data read from the file.
    """

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, encoding=ENCODING, low_memory=False, header=header)
    elif filepath.endswith('.htm'):
        df = pd.read_html(filepath, header=0)
        # If df is a list and multiple_tables=False, find the DataFrame with the most rows.
        if isinstance(df, list) and not multiple_tables:
            df_index = 1
            max_rows = 0
            for i, d in enumerate(df):
                rows = len(d.index)
                if rows > max_rows:
                    df_index = i
                    max_rows = rows
            df = df[df_index]
    else:
        df = pd.read_excel(filepath)
    if remove_unnamed:
        df = remove_heading(df)
    return df


if __name__ == '__main__':
    pass