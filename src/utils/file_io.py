# file_io.py
import csv
from src.utils.csv_configs import CSV_CONFIGS

def parse_csv(file_path, config_name):
    config = CSV_CONFIGS[config_name]
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=config["delimiter"])
        for _ in range(config["header"]):
            next(reader)
        columns = next(reader)  # Read header row
        data = [dict(zip(columns, row)) for row in reader]
    return data
