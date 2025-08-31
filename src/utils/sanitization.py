from src.utils.logging import get_logger
import pandas as pd
import numpy as np
import re
logger = get_logger(__name__)

def check_data_contents(data: pd.DataFrame) -> bool:
    """Check if the DataFrame is empty.

    Args:
        data (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the DataFrame is not empty, False otherwise.
    """
    if not data.empty:
        logger.info("DataFrame is not empty, okay to proceed.")
        return True
    logger.warning("DataFrame is empty, cannot proceed.")
    return False

def reformat_sample_names(data: pd.DataFrame) -> pd.DataFrame:
    """ _Take the sample name column and remove extra spaces, specical characters, and lower case all._

    Args:
        data (pd.DataFrame): _DataFrame containing 'sample_name' column._
    Reformating Steps:
        `clean white space`
        `remove special characters`
        `collapse multiple spaces`
        `convert to lowercase`
    Returns:
        pd.DataFrame: _cleaned 'sample_name' column, data body not touched._

    """
    data['sample_name'] = data['sample_name'].str.strip()  # Remove leading/trailing whitespace
    data['sample_name'] = data['sample_name'].str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
    data['sample_name'] = data['sample_name'].apply(lambda x: re.sub(r'\s+', ' ', x))  # Collapse multiple spaces
    data['sample_name'] = data['sample_name'].str.lower()
    
    return data

def remove_extra_space_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Remove all whitespace characters (spaces, tabs, etc.) from each cell in the specified columns of the dataframe.

    Example:

        Input:
            | sample_name  | analyte_1 | analyte_2 |
            |--------------|-----------|-----------|
            | gregory      |  < 0      | 0         |
            | low control  |           | 90        |
            | med control  |  N/A      | 90        |
            | testone      | N A       | 90        |
            | hi           | NA        | NA        |

        Output:
            | sample_name  | analyte_1 | analyte_2 |
            |--------------|-----------|-----------|
            | gregory      | <0        | 0         |
            | low control  |           | 90        |
            | med control  | N/A       | 90        |
            | testone      | NA        | 90        |
            | hi           | NA        | NA        |
    """
    # Strip whitespace
    for col in cols:
        df[col] = df[col].map(lambda x: str(x).replace(' ', '') if pd.notnull(x) else x)
    return df

def remove_string_na_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """_Remove variations of literal "NA" from the dataframe._
    
    Example table:
    
        | Input      | Output     |
        |------------|------------|
        |"N/A"       | 0.0        |
        |"NA"        | 0.0        |
        |"na"        | 0.0        |
        |"Na"        | 0.0        |
        |"nA"        | 0.0        |
        |"something" | "something"|
        
    Returns:
    
    _data frame will have NA values replaced with 0.0 type float._
    """
    # Replace N/A, NA, na, Na (case-insensitive, with or without spaces) with numeric 0.0
    for col in cols:
        df[col] = df[col].map(lambda x: 0.0 if (pd.notnull(x) and isinstance(x, str) and re.match(r'(?i)^\s*(N/A|NA|na|Na|nA)\s*$', x)) else x)
    # Remove special characters
    return df

def remove_special_characters_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    r"""
    Remove special characters from the data body, including underscores.

    List of special characters removed:
        ! @ $ % ^ & * ( ) _ + = { } [ ] : ; " ' < , > ? / \| ~ ` #

    Example:

    Input:
    +--------------+------------------------+
    | sample_name  | analyte_1              |
    +--------------+------------------------+
    | patient!1    | 10$%^&*()_+            |
    | patient@2    | 10{}[]:;"'<,>?/\|~`    |
    | patient#3    | 20                     |
    +--------------+------------------------+

    Output:
    +--------------+-----------+
    | sample_name  | analyte_1 |
    +--------------+-----------+
    | patient1     | 10        |
    | patient2     | 10        |
    | patient3     | 20        |
    +--------------+-----------+
    """
    for col in cols:
        df[col] = df[col].map(lambda x: re.sub(r'[^\da-zA-Z\s.-]', '', str(x)) if pd.notnull(x) else x)
    
    return df

def remove_empty_strings_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Convert all empty strings and None values to NaN (missing value)."""
    # Replace empty strings (after cleaning) with np.nan
    for col in cols:
        df[col] = df[col].map(lambda x: np.nan if (x == "" or x is None) else x)   
    
    return df

def replace_no_root_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """_Replace all 'no root' values with 'Invalid'
    """
    # Replace no root with 'Invalid'
    df[cols] = df[cols].replace(r'(?i)^noroot$', 'Invalid', regex=True)
    
    return df

def convert_to_numeric_data_body(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """_Force all values into numeric (float) format for consistency._
    
    """
    # Convert numeric columns to float, leave 'Invalid' as string
    for col in cols:
        df[col] = df[col].map(lambda x: float(x) if (pd.notnull(x) and x != 'Invalid') else x)

    return df

def reformat_data_body(data: pd.DataFrame) -> pd.DataFrame:
    """_Clean the table body._
    
   `Version 001:`
    
    Steps:
    
    1. Trim all existing whitespaces.
    2. Convert all existing variations of 'na' into 0 values.
    3. Remove all special characters.
    4. Replace all empty values with empty strings.
    5. Replace all 'no root' values with 'Invalid'.
    6. Convert all remaining values to numeric, force all errors to NaN.
    """
    cols = data.columns[1:]
    data = remove_extra_space_data_body(data, cols)
    data = remove_string_na_data_body(data, cols)
    data = remove_special_characters_data_body(data, cols)
    data = remove_empty_strings_data_body(data, cols)
    data = replace_no_root_data_body(data, cols)
    data = convert_to_numeric_data_body(data, cols)
    
    return data

def check_levels_present(data: pd.DataFrame) -> list:
    """_Look for anything that may resemble a control within the sequence._  

    Match detection:
    - "C[1-3]", 'Low Control', "Medium Control", "High Control", 
    - "Med Control", "VISCON", "Dil con", "DIL CON", "Dilution control"
    - NC1, NC2, NC3, PG1, PG2, PG3, CUTOFF G1, CUTOFF G2, CUTOFF G3,
    - Negative Control, Blank control
    - "UTAK", "UTAK control"
    
    """
    logger.info("Checking if quality control levels are present in the data.")
    # regular expression to check all of those levels, case insensitive.
    pattern = r"(?i)(C[1-3]|Low Control|Medium Control|High Control|Med Control|VISCON|Dil con|DIL CON|Dilution control|NC[1-3]|PG[1-3]|CUTOFF G[1-3]|Negative Control|Blank control|UTAK|UTAK control)"
    matches = [re.search(pattern, str(item)) for item in data['sample_name']]
    return [match.group() for match in matches if match]

def check_number_of_specimen(data: pd.DataFrame) -> list:
    """_Return the list of non-control like rows._
    
    """
    logger.info("Checking number of specimens in the data.")
    mismatches=[]
    # regular expression to check all of those levels, case insensitive.
    pattern = r"(?i)(C[1-3]|Low Control|Medium Control|High Control|Med Control|VISCON|Dil con|DIL CON|Dilution control|NC[1-3]|PG[1-3]|CUTOFF G[1-3]|Negative Control|Blank control|UTAK|UTAK control)"
    # find all that do not match the pattern.
    mismatches = [item for item in data['sample_name'] if not re.search(pattern, str(item))]
    
    return mismatches

def check_number_of_specimen(data: pd.DataFrame) -> list:
    """_Return the list of non-control like rows._

    """
    logger.info("Checking number of specimens in the data.")

    return []


if __name__ == "__main__":
    # call each function here
    pass