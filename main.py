from src.utils.sanitation import *
import pandas as pd

def main():

    data = pd.read_csv("sample_patients.csv")
    
    
    data_present = check_data_contents(data)
    data_sample_name_cleaned = reformat_sample_names(data)
    #cleaned_data = reformat_data_body(data_sample_name_cleaned)
    qc_levels = check_levels_present(data)
    
    print(f"Performed check on data present. Result determined: {data_present}")
    print(f"Quality control levels found: {len(qc_levels)}")

if __name__ == "__main__":  
    main()
    # run logic to perform functions