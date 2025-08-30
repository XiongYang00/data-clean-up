import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import pytest
import pandas as pd
from src.utils.sanitation import *


def test_check_data_contents_exist():
    df_not_empty = pd.DataFrame({'sample_name':['C1','C2','C3']})
    
    assert check_data_contents(df_not_empty) == True

def test_check_data_contents_empty():
    df_empty = pd.DataFrame()
    
    assert check_data_contents(df_empty) == False
    
def test_check_levels_present_exist():
    df = pd.DataFrame(
        {
            'sample_name': [
                'C1',
                'C2',
                'C3'
            ]
        }
    )
    assert check_levels_present(df) == ['C1','C2','C3']

def test_check_levels_present_empty():
    df = pd.DataFrame(
        {
            'sample_name': [
                'TEST1',
                'TEST2',
                'TEST3'
            ]
        }
    )
    assert check_levels_present(df) == []