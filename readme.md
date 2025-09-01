git clone https://github.com/XiongYang00/data-clean-up.git
pip install requirements.txt

# Data Clean-Up Project

## Overview
This project cleans and reformats patient sample CSV data using pandas, with logging, configuration, and automated testing.

## Directory Structure
- `main.py`: Main script for data cleaning.
- `requirements.txt`: Python dependencies.
- `run_all_tests.py`: Runs all unit tests and saves results.
- `config/`: Contains `csv_configs.json` for CSV parsing options.
- `log/`: Stores log files.
- `scripts/`: Environment setup scripts (`setup_env.py`, `activate_env.ps1`).
- `src/utils/`: Core modules (`sanitization.py`, `file_io.py`, `logging.py`, `csv_configs.py`).
- `tests/`: Unit tests for core modules.
- `unit_test_results/`: Markdown files with test results.
- `sample_patients.csv`, `cleaned_sample_patients.csv`: Example input/output data.

## Features
- Cleans sample names (removes whitespace, special characters, lowercases).
- Exports cleaned data to CSV.
- Custom logging with user and function info.
- Configurable CSV parsing.
- Automated environment setup and activation (Windows PowerShell).
- Automated test running and result logging.

## Setup Instructions
1. Clone the repository:
	 ```
	 git clone https://github.com/XiongYang00/data-clean-up.git
	 ```
2. Set up the virtual environment and install dependencies:
	 ```
	 python scripts/setup_env.py
	 ```
	 This will:
	 - Create a virtual environment in `venv/`
	 - Install dependencies from `requirements.txt`
	 - Open a new PowerShell window with the environment activated (Windows only)

## Usage
- Place your input CSV as `sample_patients.csv` in the root directory.
- Run the main script:
	```
	python main.py
	```
	Output will be saved as `cleaned_sample_patients.csv`.

## Testing
- Run all unit tests and save results:
	```
	python run_all_tests.py
	```
	Results are saved in `unit_test_results/`.
- Or run pytest directly:
	```
	pytest tests
	```

## Configuration
- Edit `config/csv_configs.json` to adjust CSV parsing options.

## Modules
- `src/utils/sanitization.py`: Data cleaning functions.
- `src/utils/file_io.py`: CSV export utility.
- `src/utils/logging.py`: Custom logger.
- `src/utils/csv_configs.py`: Default CSV configs.