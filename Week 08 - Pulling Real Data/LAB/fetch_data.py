
from pathlib import Path

import pandas as pd
import requests

# Right here we have the settings for the API
URL = "https://api.github.com/orgs/python/repos"
PARAMS = {"per_page": 100}
RECORDS_KEY = None

RENAME = {}

KEEP = [
    "id",
    "name",
    "full_name",
    "private",
    "description",
    "fork",
    "license_name"
]

MUST_HAVE = ["name", "full_name"]

RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"


# Here are the start of the functions
# The first function gets the data from the API 

def get_data(url, params):
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print("Could not get the data:", error)
        return None
    
# This function makes the pandas table and makes the records into rows and columns
def make_table(data, records_key):
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")


# This functions tidies the tables and returns the cleaned version
def tidy_data(df):
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df

# This function saves all the data and then outputs how many rows have been saved
def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


# This runs the program and at the end saves the table as a CSV file

if __name__ == "__main__":
    data = get_data(URL, PARAMS)

    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)

        print(table.head())
        save_data(table, RAW_FILE)

# To run this program, open the Terminal in the CST1510_CW2 folder and enter:
# python "Week 08 - Pulling Real Data/LAB/fetch_data.py"