from src.utils.sanitation import *
from src.utils.file_io import  *
import pandas as pd

def main():

    data = pd.read_csv("sample_patients.csv", keep_default_na=False)
    
    
    data_present = check_data_contents(data)
    data_sample_name_cleaned = reformat_sample_names(data)
    cleaned_data = reformat_data_body(data_sample_name_cleaned)
    #qc_levels = check_levels_present(cleaned_data)
    export_dataframe_to_csv(cleaned_data, "cleaned_sample_patients.csv", index=False)
    #print(f"Performed check on data present. Result determined: {data_present}")
    #print(f"Quality control levels found: {len(qc_levels)}")

if __name__ == "__main__":
    main()
    # run logic to perform functions