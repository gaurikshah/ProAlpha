import pandas as pd
from pathlib import Path
import openpyxl
import os
import warnings


def check_existing_prices_files(folder_path):
    existing_instruments = os.listdir(folder_path)
    existing_instruments = list(filter(lambda f: f.endswith('.csv'), existing_instruments))
    existing_instruments = list(map(lambda x: x.replace(".csv", ""), existing_instruments))
    existing_instruments = [x.upper() for x in existing_instruments]

    return existing_instruments


def price_data_csv_update(file_name="closing_prices.xlsx"):

    folder_path_closing_prices = Path().absolute().joinpath("Input Data\proalpha_data")
    folder_path_instrument_prices = Path().absolute().joinpath("Input Data\instrument_daily_prices")

    closing_prices_file = folder_path_closing_prices / file_name

    wb = openpyxl.load_workbook(closing_prices_file)
    sheet_names = wb.get_sheet_names()
    ws = wb.get_sheet_by_name(sheet_names[0])
    closing_prices = pd.DataFrame(ws.values)

    closing_prices.columns = closing_prices.iloc[0]
    closing_prices.columns = [x.upper() for x in closing_prices.columns]
    closing_prices.drop(0, inplace=True)
    closing_prices.set_index(closing_prices.columns[0], drop=True, inplace=True)
    closing_prices.dropna()

    existing_instruments = check_existing_prices_files(folder_path_instrument_prices)

    for i in closing_prices.columns:
        if i in existing_instruments:
            existing_file = folder_path_instrument_prices / f"{i}.csv"
            existing_prices = pd.read_csv(existing_file, index_col=0)
            existing_prices.index = pd.to_datetime(existing_prices.index)
            existing_prices = existing_prices.dropna()
            closing_prices_current_instrument = pd.to_numeric(closing_prices[i].dropna(), errors="coerce")
            closing_prices_current_instrument = closing_prices_current_instrument.dropna()
            existing_prices = existing_prices[i].append(closing_prices_current_instrument)
            existing_prices = existing_prices[~existing_prices.index.duplicated(keep='first')]
            existing_prices.name = i
            existing_prices_file_name = f"{i}.csv"
            existing_prices.to_csv(folder_path_instrument_prices / existing_prices_file_name)
        else:
            a = i.replace("/", "-")
            new_file_name = f"{a}.csv"
            closing_prices_current_instrument = pd.to_numeric(closing_prices[i].dropna(), errors="coerce")
            closing_prices_current_instrument = closing_prices_current_instrument.dropna()
            closing_prices_current_instrument.to_csv(folder_path_instrument_prices.joinpath(new_file_name), index=True)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    price_data_csv_update()
