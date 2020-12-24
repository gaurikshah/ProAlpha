from pathlib import Path
import pandas as pd
import os
import openpyxl
from collections import namedtuple


def convert_datetime(data_frame):
    cols = data_frame.select_dtypes('datetime64')
    data_frame[cols.columns] = cols.apply(lambda x: x.dt.strftime('%Y-%m-%d'))

    return data_frame


def csv_creation(data_frames, dir_name):
    output_dir=Path().absolute().joinpath(dir_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in data_frames:
        output_file = i.name + '.csv'
        i.to_csv(output_dir / output_file)  # can join path elements with / operator


def reading_price_data_from_csv(file_path):
    price_data = pd.read_csv(file_path)
    price_data.set_index("Dates", inplace=True)
    price_data.columns = ["Open", "High", "Low", "Close", "Volume"]
    price_data.index = pd.to_datetime(price_data.index, format="%d-%m-%Y")

    return price_data


def reading_trades_from_csv(file_path):
    trades = pd.read_csv(file_path, header=0, parse_dates=True)
    trades["Date"] = pd.to_datetime(trades["Date"], format="%d-%m-%Y")

    return trades


def import_price_data_from_csv_files(folder_path, symbols):
    price_data = {}

    for symbol in symbols:
        price_data_name = pd.read_csv(folder_path.joinpath( symbol + '.csv'))
        price_data_name.set_index("Dates", inplace=True)
        price_data_name.columns = ["Open", "High", "Low", "Close", "Volume"]
        price_data_name.index = pd.to_datetime(price_data_name.index, format="%d-%m-%Y")

        price_data[symbol] = price_data_name

    return price_data

def import_all_price_data_from_csv_files(folder_path):

    symbols = os.listdir(folder_path)
    symbols = list(filter(lambda f: f.endswith('.csv'), symbols))

    symbols = list(map(lambda x : x.replace(".csv", ""), symbols))

    price_data = import_price_data_from_csv_files(folder_path, symbols)

    return price_data

def excel_creation(data_frames, dir_name,excel_name):

    output_dir=Path().absolute().joinpath(dir_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_name=excel_name+".xlsx"
    output_file=output_dir/output_file_name

    with pd.ExcelWriter(output_file, engine="openpyxl",datetime_format='DD/MM/YYYY',float_format="#,##0;-#,[RED]#,##0") as writer:
        for n, df in enumerate(data_frames):
            df.to_excel(writer, sheet_name=data_frames[n].name)
        writer.save()

def reading_list_of_strats_from_excel(input_file_path):

    input_file_name = "Strategies.xlsx"
    input_file = input_file_path / input_file_name

    strategies=read_from_excel(input_file)

    strategies_data=strategies["Strategies"]


    strategy_list=iternamedtuples(strategies_data)

    return strategy_list

def iternamedtuples(strategies_data):

    strategy=namedtuple("strategy",["Strategy","Period","Parameters"])
    strategy_list=[]
    for row in strategies_data.index:

        period=strategies_data.loc[row][0]

        strategy_1=strategy(row,period,strategies_data.loc[row][1:].tolist())

        strategy_list.append(strategy_1)

    return strategy_list


def read_from_excel(input_file_path):

    wb=openpyxl.load_workbook(input_file_path)

    sheet_name=wb.get_sheet_names()
    dataframes={}

    for sheet in sheet_name:
        dataframes[sheet]=pd.DataFrame(wb.get_sheet_by_name(sheet).values)
        dataframes[sheet].columns=dataframes[sheet].iloc[0]
        dataframes[sheet].drop(0,inplace=True)
        dataframes[sheet].set_index(dataframes[sheet].columns[0],drop=True,inplace=True)

    return dataframes
