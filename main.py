from src.utils.sanitization import *
from src.utils.dataframe_match_comparison import *
from src.utils.file_io import  *
import pandas as pd

def main():

    data = import_dataframe_from_csv()
    data_present = check_data_contents(data)
    data_sample_name_cleaned = reformat_sample_names(data)
    cleaned_data = reformat_data_body(data_sample_name_cleaned)
    #qc_levels = check_levels_present(cleaned_data)
    export_dataframe_to_csv(cleaned_data, "cleaned_sample_patients.csv", index=False)

def file_comparison():
    """
    Compare two cleaned CSV files using pandas testing utilities.
    Checks for exact matches in columns, dtypes, and values.
    Returns a traceable analysis or raises AssertionError if not equal.
    """
    results = compare_cleaned_dataframes("cleaned_sample_patients.csv", "cleaned_sample_patients.csv")
    #print(results)
    pass

if __name__ == "__main__":
    #main()
    # run logic to perform functions
    file_comparison()