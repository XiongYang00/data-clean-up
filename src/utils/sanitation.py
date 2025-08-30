from src.utils.logging import get_logger
import pandas as pd
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

def check_levels_present(data: pd.DataFrame) -> list:
    """
    Count the number of quality control levels present in the data.
    Regular expressions to detect:
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

if __name__ == "__main__":
    # call each function here
    pass