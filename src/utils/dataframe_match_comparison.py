
import numpy as np

def compare_dtype(s1, s2):
    return s1.dtype == s2.dtype

def compare_row_count(s1, s2):
    return (len(s1), len(s2))

def compare_values(s1, s2, tolerance=0.0):
    mismatches = []
    dtype = s1.dtype
    for idx in range(min(len(s1), len(s2))):
        v1 = s1.iloc[idx]
        v2 = s2.iloc[idx]
        if pd.isna(v1) and pd.isna(v2):
            match = True
        elif pd.api.types.is_numeric_dtype(dtype) and not pd.isna(v1) and not pd.isna(v2):
            if tolerance > 0:
                match = np.isclose(v1, v2, rtol=tolerance)
            else:
                match = v1 == v2
        else:
            match = v1 == v2
        if not match:
            mismatches.append(idx)
    return {
        "num_mismatches": len(mismatches),
        "mismatched_indices": mismatches
    }
class ComparisonAnalysis:
    def export_comparisons_excel(self, output_path="comparison_reports/column_comparisons.xlsx"):
        import os
        import pandas as pd
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        a = self.analysis
        df1 = pd.read_csv(a['file_1'])
        df2 = pd.read_csv(a['file_2'])
        common_cols = set(df1.columns) & set(df2.columns)
        with pd.ExcelWriter(output_path) as writer:
            for col in common_cols:
                rows = []
                for idx in range(min(len(df1), len(df2))):
                    val1 = df1.iloc[idx][col]
                    val2 = df2.iloc[idx][col]
                    match = val1 == val2
                    rows.append({
                        "Index": idx,
                        "File_1": val1,
                        "File_2": val2,
                        "Match": match
                    })
                pd.DataFrame(rows).to_excel(writer, sheet_name=col, index=False)
        print(f"Saved all column comparisons to {output_path}")

    def __init__(self, analysis: dict):
        self.analysis = analysis

    def display(self):
        a = self.analysis
        print(f"\nFile 1: {a['file_1']}")
        print(f"File 2: {a['file_2']}\n")
        print("Column Names Match:", a['column_match'])
        print("Data Types Match:", a['dtype_match'])
        print("\nColumns in File 1:", a['columns_file1'])
        print("Columns in File 2:", a['columns_file2'])
        print("\nData Types in File 1:")
        for k, v in a['dtypes_file1'].items():
            print(f"  {k}: {v}")
        print("Data Types in File 2:")
        for k, v in a['dtypes_file2'].items():
            print(f"  {k}: {v}")

        print("\nSeries Comparison:")
        for col, comp in a['series_comparison'].items():
            print(f"\nColumn: {col}")
            print(f"  Dtype Match: {comp['dtype_match']}")
            print(f"  Exact Match: {comp['num_mismatches'] == 0}")
            print(f"  Number of Mismatches: {comp['num_mismatches']}")
            if comp['num_mismatches'] > 0:
                print(f"  Mismatched Indices: {comp['mismatched_indices']}")

        print("\nDataFrame Match:", a['dataframe_match'])
        print("Result:", a['result'])
        if not a['dataframe_match'] and 'error' in a:
            print("Error:", a['error'])


import pandas as pd
from pandas.testing import assert_frame_equal
import tkinter as tk
from tkinter import filedialog

def compare_cleaned_dataframes(file_1: str = None, file_2: str = None) -> dict:
    """
    Compare two cleaned CSV files for column names, dtypes, and values.
    If file paths are not provided, prompt user to select files via file explorer.
    Returns a detailed analysis for each column/series, even if DataFrames match.
    """
    # File selection via file explorer if paths not provided
    if not file_1 or not file_2:
        root = tk.Tk()
        root.withdraw()
        print("Select the first cleaned CSV file...")
        file_1 = filedialog.askopenfilename(title="Select first cleaned CSV file", filetypes=[("CSV files", "*.csv")])
        print("Select the second cleaned CSV file...")
        file_2 = filedialog.askopenfilename(title="Select second cleaned CSV file", filetypes=[("CSV files", "*.csv")])


    df1 = pd.read_csv(file_1)
    df2 = pd.read_csv(file_2)
    # Treat all empty strings and NaN as NaN for comparison
    df1 = df1.replace("", pd.NA)
    df2 = df2.replace("", pd.NA)

    analysis = {
        "file_1": file_1,
        "file_2": file_2,
        "columns_file1": list(df1.columns),
        "columns_file2": list(df2.columns),
        "dtypes_file1": df1.dtypes.astype(str).to_dict(),
        "dtypes_file2": df2.dtypes.astype(str).to_dict(),
        "column_match": set(df1.columns) == set(df2.columns),
        "dtype_match": df1.dtypes.equals(df2.dtypes),
        "series_comparison": {}
    }


    # Per-series modular comparison
    common_cols = set(df1.columns) & set(df2.columns)
    for col in common_cols:
        s1 = df1[col]
        s2 = df2[col]
        dtype_match = compare_dtype(s1, s2)
        row_counts = compare_row_count(s1, s2)
        value_result = compare_values(s1, s2, tolerance=0.20)
        analysis["series_comparison"][col] = {
            "dtype_match": dtype_match,
            "row_counts": row_counts,
            "num_mismatches": value_result["num_mismatches"],
            "mismatched_indices": value_result["mismatched_indices"]
        }

    # DataFrame-level comparison
    try:
        assert_frame_equal(df1, df2, check_dtype=True, check_like=False)
        analysis["dataframe_match"] = True
        analysis["result"] = "DataFrames are exactly equal."
    except AssertionError as e:
        analysis["dataframe_match"] = False
        analysis["result"] = "DataFrames are NOT equal."
        analysis["error"] = str(e)

    # Display formatted report using ComparisonAnalysis
    report = ComparisonAnalysis(analysis)
    report.display()
    report.export_comparisons_excel()
    return analysis