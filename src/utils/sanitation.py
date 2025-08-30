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

def reformat_data_body(data: pd.DataFrame) -> pd.DataFrame:
    """_Clean the table body_"""
    cols = data.columns[1:]
    # Strip whitespace
    for col in cols:
        data[col] = data[col].map(lambda x: str(x).strip() if pd.notnull(x) else x)
    # Remove special characters
    for col in cols:
        data[col] = data[col].map(lambda x: re.sub(r'[^\w\s.-]', '', str(x)) if pd.notnull(x) else x)
    # Replace empty strings with np.nan
    data[cols] = data[cols].replace('', np.nan)
    # Replace N/A, NA, na, Na with 0
    data[cols] = data[cols].replace(r'(?i)^(N/A|NA|na|Na)$', 0, regex=True)
    # Replace no root with 'Invalid'
    data[cols] = data[cols].replace(r'(?i)^no root$', 'Invalid', regex=True)
    # Convert numeric columns to float, leave 'Invalid' as string
    for col in cols:
        data[col] = data[col].map(lambda x: float(x) if (pd.notnull(x) and x != 'Invalid') else x)
    return data

def check_levels_present(data: pd.DataFrame) -> list:
    """_Look for anything that may resemble a control within the sequence._  
    Args:
        data (pd.DataFrame): _DataFrame containing 'sample_name' column._

    Match detection:
    - "C[1-3]", 'Low Control', "Medium Control", "High Control", 
    - "Med Control", "VISCON", "Dil con", "DIL CON", "Dilution control"
    - NC1, NC2, NC3, PG1, PG2, PG3, CUTOFF G1, CUTOFF G2, CUTOFF G3,
    - Negative Control, Blank control
    - "UTAK", "UTAK control"
    
    Returns:
        list: _a list of samples that match potential control material._
    
    """
    logger.info("Checking if quality control levels are present in the data.")
    # regular expression to check all of those levels, case insensitive.
    pattern = r"(?i)(C[1-3]|Low Control|Medium Control|High Control|Med Control|VISCON|Dil con|DIL CON|Dilution control|NC[1-3]|PG[1-3]|CUTOFF G[1-3]|Negative Control|Blank control|UTAK|UTAK control)"
    matches = [re.search(pattern, str(item)) for item in data['sample_name']]
    return [match.group() for match in matches if match]

def check_number_of_specimen(data: pd.DataFrame) -> list:

    return []


if __name__ == "__main__":
    # call each function here
    pass