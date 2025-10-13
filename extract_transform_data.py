'''Extract, Transform, Load (ETL) process for football data.'''
import glob
import os
from datetime import datetime

import pandas as pd

TARGET_FILE = "transformed_data.csv"
SECOND_DIVISION_FILE = "es.2.csv"
LOG_FILE = "log_file.txt"


def extract_from_csv(file_to_process):
    """Extract data from a CSV file.

    Args:
        file_to_process (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.
    """
    dataframe = pd.read_csv(file_to_process)
    return dataframe


def extract():
    '''Extract data from all files except the target file'''
    # create an empty data frame to hold extracted data
    extracted_data = pd.DataFrame(
        columns=[
            'Round',
            'Date',
            'Team 1',
            'FT',
            'Team 2',
        ])
    # process all csv files recursively, except the target file
    for csvfile in glob.glob("**/*.csv", recursive=True):
        # compare basenames so files nested in datasets/... are also excluded if needed
        if os.path.basename(csvfile) not in (TARGET_FILE, SECOND_DIVISION_FILE):
            extracted_data = pd.concat([extracted_data, pd.DataFrame(
                extract_from_csv(csvfile))], ignore_index=True)

    return extracted_data


def transform(data):
    '''Transform the extracted data.'''
    # Convert 'Date' column to datetime format (accept day-first and be tolerant)
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

    # Split 'FT' column into 'FT Team 1' and 'FT Team 2'
    ft_split = data['FT'].str.split('-', expand=True)
    ft_split = pd.concat([ft_split[0].rename('FT Team 1'),
                          ft_split[1].rename('FT Team 2')], axis=1)
    data = pd.concat([data, ft_split], axis=1)
    data.drop(columns=['FT'], inplace=True)

    return data


def load_data(target_file, data):
    '''Load transformed data into the target file.'''
    data.to_csv(target_file, index=False)


def log_progress(message):
    """
    Logs a progress message with a timestamp to the specified log file.

    Args:
        message (str): The message to log.

    Notes:
        - The timestamp format is 'Year-Monthname-Day-Hour-Minute-Second'.
        - The log entry is appended to the log file, each entry on a new line.
        - Requires 'datetime' and 'log_file' to be defined in the scope.
    """
    timestamp_format = '%Y-%B-%d-%H:%M:%S'  # Year-Monthname-Day-Hour-Minute-Second (%B = full month name)
    now = datetime.now()  # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(timestamp + ',' + message + '\n')


# Log the initialization of the ETL process
log_progress("ETL Job Started")

# Log the beginning of the Extraction process
log_progress("Extract phase Started")
extracted = extract()

# Log the completion of the Extraction process
log_progress("Extract phase Ended")

# Log the beginning of the Transformation process
log_progress("Transform phase Started")
transformed_data = transform(extracted)
print("Transformed Data")
print(transformed_data)

# Log the completion of the Transformation process
log_progress("Transform phase Ended")

# Log the beginning of the Loading process
log_progress("Load phase Started")
load_data(TARGET_FILE, transformed_data)

# Log the completion of the Loading process
log_progress("Load phase Ended")

# Log the completion of the ETL process
log_progress("ETL Job Ended")
