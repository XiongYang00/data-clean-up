import pandas as pd
import os

def export_dataframe_to_csv(df: pd.DataFrame, file_path: str = None, index: bool = False):
    """
    Export a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to export.
        file_path (str): Path to the output CSV file. If None, saves as 'output.csv' in current directory.
        index (bool): Whether to write row names (index).
    """
    if file_path is None:
        file_path = os.path.join(os.getcwd(), 'output.csv')
    df.to_csv(file_path, index=index, encoding='utf-8')
