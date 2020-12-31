import pandas as pd
import openpyxl as xl
import numpy as np
from pathlib import Path
from Individual_Trades import Individual_Trades
import collections
from Trade_Generation import creating_individual_trade, creating_individual_trade_db
from Timeframe_Manipulation import series_resampling as tm
from PNL_Generation import pnl_generation as pg
import my_funcs
import warnings

def set_dataframe(df):
    df.columns=df.loc[0]
    df.drop(0,inplace=True)
    df.set_index("Dates",inplace=True)

if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    baseamount = 10000000

    current_folder_path = Path().absolute().joinpath("Data")
    nifty_price_data = current_folder_path / "Price_Data/Nifty Index.csv"
    trade_file_path = current_folder_path / "proalpha_data/trade_data_sample.csv"

    price_data_file= current_folder_path / "proalpha_data/OHLC.xlsx"

    wb = xl.load_workbook(price_data_file)

    sheet_name=wb.get_sheet_names()

    data={}

    for i in sheet_name:
        data[i]=pd.DataFrame(wb.get_sheet_by_name(i).values)
        set_dataframe(data[i])

    symbols = data["CLOSE"].columns

    price_data={}

    for i in symbols:

        a = pd.DataFrame()
        a["Open"]=data["OPEN"][i]
        a["High"] = data["HIGH"][i]
        a["Low"] = data["LOW"][i]
        a["Close"] = data["CLOSE"][i]
        a["Volume"]=0
        a.replace("#N/A N/A",np.nan,inplace=True)
        a.dropna(subset=["Close"],inplace=True)
        a.fillna(method="bfill",axis=1)

        price_data[i]=a

    universal_dates = price_data["Nifty INDEX"].index

    individual_trade_list = my_funcs.reading_trades_from_csv(trade_file_path)



    individual_trade_list.columns = ["Account", "Strategy", "Date", "Price", "Side", "Contract", "Contract_Type",
                                     "Lots", "Lot_Size", "Qty", "Trading_Cost", "Strike_Price"]

    account_list = individual_trade_list["Account"].unique()
    strategy_list = individual_trade_list["Strategy"].unique()
    symbols = individual_trade_list["Contract"].unique()


    #price_data = my_funcs.import_price_data_from_csv_files(current_folder_path / "Price_Data", symbols)

    pnl_series={}

    pnl_series_strategy=pd.DataFrame(0,columns=symbols,index=universal_dates)
    gross_exposure_strategy=pd.DataFrame(0,columns=symbols,index=universal_dates)
    net_exposure_strategy=pd.DataFrame(0,columns=symbols,index=universal_dates)

    for account in account_list:
        for symbol in symbols:

            if Individual_Trades.trade_register!=[]:
                Individual_Trades.trade_register[0].re_initialise()

            trade_list_to_pass = individual_trade_list[
                (individual_trade_list["Account"] == account) & (individual_trade_list["Contract"] == symbol)]
            trade_list_to_pass.drop(["Account","Strategy"],axis=1,inplace=True)
            trade_list_to_pass.reset_index(drop=True,inplace=True)

            trade_register = creating_individual_trade_db.creating_individual_trade_db(trade_list_to_pass)

            pnl_series_1, _ = pg.pnl_timeseries_multiple_strategy_trade(trade_register, price_data,
                                                                      universal_dates, baseamount)

            pnl_series_strategy[symbol]=pnl_series_1["Daily PNL"]
            gross_exposure_strategy[symbol] = pnl_series_1["Gross Exposure"]
            net_exposure_strategy[symbol] = pnl_series_1["EOD Net Exposure"]

        pnl_series_strategy["Total"] =pnl_series_strategy.sum(axis=1)
        pnl_series_strategy.loc["Total"] = pnl_series_strategy.sum(axis=0)

        gross_exposure_strategy["Total"] = gross_exposure_strategy.sum(axis=1)
        net_exposure_strategy["Total"] = net_exposure_strategy.sum(axis=1)

        pnl_series[account] = [pnl_series_strategy,gross_exposure_strategy,net_exposure_strategy]

    for account in account_list:
        pnl_series[account][0].name = "PNL Series "+ account
        pnl_series[account][1].name = "Gross exposure Series " + account
        pnl_series[account][2].name = "Net exposure Series " + account
        to_be_saved_as_csv = [ pnl_series[account][0] ,pnl_series[account][1],pnl_series[account][2]]

        my_funcs.excel_creation(to_be_saved_as_csv, "Pro_Alpha_PNL", account)

