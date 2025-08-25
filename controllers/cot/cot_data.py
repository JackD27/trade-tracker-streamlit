import datetime
import io
import os
import zipfile

import pandas as pd
import requests
from pandas import DataFrame

from .cot_constants import RENAME_COLUMNS, MARKETS_TO_KEEP, MARKET_NAME_MAP, MARKET_TYPE

NOW: datetime = datetime.datetime.now()
CURRENT_YEAR: int = NOW.year
PREVIOUS_YEAR: int = CURRENT_YEAR - 1
YEAR_BEFORE_PREVIOUS: int = CURRENT_YEAR - 2
DATA_DIR: str = "data"
ANNUAL_FILE = os.path.join(DATA_DIR, "annual.xls")

os.makedirs(DATA_DIR, exist_ok=True)

def update_final_parsed_data(output_file: str = f"{DATA_DIR}/final_cot_data.csv") -> None:
    print("Updating COT data...")
    two_years_ago_csv = __create_year_data(YEAR_BEFORE_PREVIOUS)
    two_years_ago_csv = two_years_ago_csv[two_years_ago_csv['Date'] >= f"{YEAR_BEFORE_PREVIOUS}-06-01"]
    prev_csv = __create_year_data(PREVIOUS_YEAR)
    curr_csv = __create_year_data(CURRENT_YEAR)

    final_df = pd.concat([prev_csv, curr_csv, two_years_ago_csv], ignore_index=True)
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    final_df['ReleaseDate'] = pd.to_datetime(final_df['Date']) + pd.to_timedelta(3, unit='D')
    final_df.sort_values(by='ReleaseDate', ascending=False, inplace=True)
    final_df.to_csv(output_file, index=False)
    if os.path.exists(ANNUAL_FILE):
        os.remove(ANNUAL_FILE)
    print("Update complete.")

def get_final_parsed_data_no_prev(output_file: str = f"{DATA_DIR}/final_cot_data.csv") -> DataFrame:
    return os.path.exists(output_file) and pd.read_csv(output_file)

def __download_and_extract_zip(year: int) -> None:
    url = f'https://www.cftc.gov/files/dea/history/dea_fut_xls_{year}.zip'
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to download data for year {year}: Status {response.status_code}")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(DATA_DIR)

def __parse_cot_data(file_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_name)
    df = df[list(RENAME_COLUMNS.keys())]
    df.rename(columns=RENAME_COLUMNS, inplace=True)
    df = df[df['Market_Names'].isin(MARKETS_TO_KEEP)]
    df['Net_Position'] = df['NonComm_Long'] - df['NonComm_Short']
    df['Market_Names'] = df['Market_Names'].map(MARKET_NAME_MAP)
    df['Market_Type'] = df['Market_Names'].map(MARKET_TYPE)
    df['Total'] = df['NonComm_Long'] + df['NonComm_Short']
    return df

def __create_year_data(year: int) -> DataFrame:
    specific_year = os.path.join(DATA_DIR, f"{year}_cot_data.csv")

    # Comment this line to download data again.
    if os.path.exists(specific_year) and year != CURRENT_YEAR:
        print(f"Data for year {year} already exists. Loading from file.")
        return pd.read_csv(specific_year)


    __download_and_extract_zip(year)
    df = __parse_cot_data(ANNUAL_FILE)
    print(f"Processing data for year {year}...")
    df.to_csv(specific_year, index=False)
    return df

def get_cot_data(year: int) -> DataFrame:
    return os.path.exists(f"{DATA_DIR}/{year}_cot_data.csv") and pd.read_csv(f"{DATA_DIR}/{year}_cot_data.csv")


