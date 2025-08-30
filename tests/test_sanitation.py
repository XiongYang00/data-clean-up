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

def test_reformat_sample_names():
    df = pd.DataFrame(
        {
            'sample_name': [
                'Gregory ',
                'Low  Control',
                ' Med Control',
                'testone!',
                'hi<'
            ]
        }
    )
    expected_df = pd.DataFrame(
        {
            'sample_name': [
                'gregory',
                'low control',
                'med control',
                'testone',
                'hi'
            ]
        }
    )
    pd.testing.assert_frame_equal(reformat_sample_names(df), expected_df)


def test_remove_extra_space_data_body():
    df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
            ],
            'analyte_1': [
                " NA",
                "N A",
                " 20"
            ]
            
        }
    )
    
    expected_df  = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
            ],
            'analyte_1': [
                "NA",
                "NA",
                "20"
            ]
        }
    )
    pd.testing.assert_frame_equal(remove_extra_space_data_body(df, ['analyte_1']), expected_df)

def test_remove_string_na_data_body():
    df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
                'patient 4',
                'patient 5',
            ],
            'analyte_1': [
                "N/A",
                "NA",
                "na",
                "Na",
                "nA"
            ]
        }
    )
    expected_df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
                'patient 4',
                'patient 5',
            ],
            'analyte_1': [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0
            ]
        }
    )
    pd.testing.assert_frame_equal(remove_string_na_data_body(df, ['analyte_1']),expected_df)
    
def test_remove_special_characters_data_body():

    df = pd.DataFrame(
        {
            'sample_name': [
                'patient!1',
                'patient@2',
                'patient#3',
            ],
            'analyte_1': [
                "10$%^&*()_+",
                "10{}[]:;\"'<,>?/\\|~`",
                "20"
            ]
        }
    )
    expected_df = pd.DataFrame(
        {
            'sample_name': [
                'patient!1',
                'patient@2',
                'patient#3',
            ],
            'analyte_1': [
                "10",
                "10",
                "20"
            ]
        }
    )
    pd.testing.assert_frame_equal(remove_special_characters_data_body(df,['analyte_1']), expected_df)

def test_remove_empty_strings_data_body():
    
    pass
def test_replace_no_root_data_body():
    
    pass

def test_convert_to_numeric_data_body():
    
    pass

def test_reformat_data_body():
    df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
                'patient 4',
                'patient 5',
                'patient 6',
                'patient 7',
                'patient 8',
                'patient 9',
                'patient 10'
            ],
            'analyte_1':["< 0" ,""," N/A","Na","NA"," 23.4 ","45.6!","noroot","#100","$200"],
            'analyte_2':["0" ,"90", 90,"90","NA"," 23.4 ","45.6!","noroot","#100","$200"]
        }
    )
    
    expected_df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
                'patient 4',
                'patient 5',
                'patient 6',
                'patient 7',
                'patient 8',
                'patient 9',
                'patient 10'
            ],
            'analyte_1': [0.0, np.nan, 0.0, 0.0, 0.0, 23.4, 45.6, "Invalid", 100.0, 200.0],
            'analyte_2': [0.0, 90.0, 90, 90.0, 0.0, 23.4, 45.6, "Invalid", 100.0, 200.0]
        }
    )
    result_df = reformat_data_body(df)
    pd.testing.assert_frame_equal(result_df, expected_df)
    return

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