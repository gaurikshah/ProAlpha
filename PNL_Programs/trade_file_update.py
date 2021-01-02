import pandas as pd
import warnings
import openpyxl
from pathlib import Path
import my_funcs

def reading_trades_from_sheet(ws):

    trades_data = pd.DataFrame(ws.values)
    trades_data.drop(0,inplace=True)
    trades_data=trades_data[2:12]

    return trades_data


def trade_file_update(file_name="trade_data.xlsx"):

    folder_path_trade_file=Path().absolute().joinpath("Input Data\proalpha_data")
    folder_path_trade_file_existing=Path().absolute().joinpath("Input Data\Trade file")


    existing_trades_file_name = folder_path_trade_file_existing / "Trades.csv"
    trades_to_update_file_name= folder_path_trade_file / file_name


    new_trade_file_columns=["Account","Expiry","Date","Bloom Code","System Code","Lots","Net Price","Trigger","Remarks","Lot Size"]
    existing_trades_columns=["Account","Strategy","Date","Price","Side","Contract","Contract_Type","Lots","Qty","Trading_Cost","Strike_Price","Broker",
                              "Brokerage","Other_cost","Trigger_price","Impact_Cost"]

    wb = openpyxl.load_workbook(trades_to_update_file_name)
    sheet_names = wb.get_sheet_names()
    ws = wb.get_sheet_by_name(sheet_names[0])

    new_trades_data = pd.DataFrame(ws.values)
    new_trades_data.drop(0, inplace=True)
    new_trades_data = new_trades_data[new_trades_data.columns[2:12]]
    new_trades_data.columns = new_trade_file_columns
    new_trades_data.dropna(subset="Bloom Code",inplace=True)
    new_trades_data.replace(None,0)

    wb.close()

    existing_trades_data = pd.read_csv(existing_trades_file_name,header=0)
    existing_trades_data.drop(0, inplace=True)
    #es_trade_data.columns = new_trade_file_columns





if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    trade_file_update("trade_data_sample.xlsx")
