import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import pytest
import pandas as pd
import numpy as np
from src.utils.sanitization import *

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
    # Test data with various spacing issues - only analyte_1 should be cleaned
    df = pd.DataFrame(
        {
            'sample_name': [
                '  patient 1  ',  # This should NOT be cleaned
                'patient  2',    # This should NOT be cleaned
                '  patient 3',   # This should NOT be cleaned
            ],
            'analyte_1': [
                " NA ",
                "N  A",
                " 20 "
            ]
            
        }
    )
    
    expected_df  = pd.DataFrame(
        {
            'sample_name': [
                '  patient 1  ',  # Unchanged because not in cols list
                'patient  2',     # Unchanged because not in cols list
                '  patient 3',    # Unchanged because not in cols list
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

    df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
            ],
            'analyte_1': [
                "",
                "",
                ""
            ]
        }
    )

    expected_df = pd.DataFrame(
        {
            'sample_name': [
                'patient 1',
                'patient 2',
                'patient 3',
            ],
            'analyte_1': [
                np.nan,
                np.nan,
                np.nan
            ]
        }
    )

    pd.testing.assert_frame_equal(remove_empty_strings_data_body(df,['analyte_1']),expected_df)
    
def test_replace_no_root_data_body():
    df = pd.DataFrame(
        {
            'sample_name': [
                'patient!1',
                'patient@2',
                'patient#3',
            ],
            'analyte_1': [
                "noroot",
                "noroot",
                "noroot"
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
                "Invalid",
                "Invalid",
                "Invalid"
            ]
        }
    )    
    
    pd.testing.assert_frame_equal(replace_no_root_data_body(df, ['analyte_1']),expected_df)

def test_convert_to_numeric_data_body():
    df = pd.DataFrame(
        {
            'sample_name': [
                'patient!1',
                'patient@2',
                'patient#3',
            ],
            'analyte_1': [
                10,
                "10",
                "Invalid"
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
                10.0,
                10.0,
                "Invalid"
            ]
        }
    )

    pd.testing.assert_frame_equal(convert_to_numeric_data_body(df,['analyte_1']),expected_df)

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

def test_check_levels_present_exist():
    df = pd.DataFrame(
        {
            'sample_name': [
                'C1',
                'C2',
                'C3',
                '109238910',
                '123123993',
                '2131445523',
                'C1',
                '13412345'
            ]
        }
    )
    
    assert check_levels_present(df) == ['C1','C2','C3','C1']

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

# Edge case tests
def test_empty_dataframe_handling():
    """Test that functions handle empty DataFrames gracefully"""
    empty_df = pd.DataFrame()
    
    # Test functions that should handle empty DataFrames
    assert check_data_contents(empty_df) == False
    
    # Note: reformat_sample_names requires 'sample_name' column to exist
    # so we test with a DataFrame that has the required column but no rows
    empty_with_columns = pd.DataFrame(columns=['sample_name'])
    result = reformat_sample_names(empty_with_columns)
    assert result.empty
    
def test_single_row_dataframe():
    """Test functions with single row DataFrames"""
    single_row_df = pd.DataFrame({'sample_name': ['TEST PATIENT!'], 'analyte_1': ['10.5']})
    
    result = reformat_sample_names(single_row_df)
    expected = pd.DataFrame({'sample_name': ['test patient'], 'analyte_1': ['10.5']})
    pd.testing.assert_frame_equal(result, expected)

def test_missing_columns():
    """Test functions with missing expected columns"""
    df_no_sample_name = pd.DataFrame({'other_col': ['value1', 'value2']})
    
    # This will raise a KeyError - the function doesn't handle missing columns gracefully
    # Let's test that the error is raised as expected
    with pytest.raises(KeyError):
        reformat_sample_names(df_no_sample_name)

def test_mixed_data_types():
    """Test functions with mixed data types"""
    mixed_df = pd.DataFrame({
        'sample_name': ['patient 1', 'patient 2'],
        'analyte_1': [123, 'abc'],  # Mixed numeric and string
        'analyte_2': [np.nan, '']   # Mixed NaN and empty string
    })
    
    # Test that remove_empty_strings_data_body handles mixed types
    result = remove_empty_strings_data_body(mixed_df, ['analyte_2'])
    assert pd.isna(result.loc[1, 'analyte_2'])  # Empty string should become NaN

def test_very_large_strings():
    """Test functions with very large string values"""
    large_string = 'x' * 1000  # 1000 character string
    df = pd.DataFrame({
        'sample_name': ['patient 1'],
        'analyte_1': [large_string + '!!!']
    })
    
    result = remove_special_characters_data_body(df, ['analyte_1'])
    assert result.loc[0, 'analyte_1'] == large_string

def test_unicode_and_special_encoding():
    """Test functions with Unicode characters"""
    unicode_df = pd.DataFrame({
        'sample_name': ['patïent 1', 'patieñt 2'],
        'analyte_1': ['tëst', 'tést']
    })
    
    result = reformat_sample_names(unicode_df)
    expected = pd.DataFrame({
        'sample_name': ['patïent 1', 'patieñt 2'],
        'analyte_1': ['tëst', 'tést']
    })
    pd.testing.assert_frame_equal(result, expected)