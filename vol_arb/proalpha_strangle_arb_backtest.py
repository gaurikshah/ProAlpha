import pandas as pd
import numpy as np
import py_vollib.black.implied_volatility as black_model_iv
import warnings
from pathlib import Path
import my_funcs


def import_data(input_file_path):
    data = my_funcs.read_from_excel(input_file_path)

    expiry_dates = data["Expiry"]
    daily_prices = data["Daily_prices"]
    futures_prices = data["Futures_prices"]
    strike_prices = data["Strike_prices"]
    call_prices = data["Call_prices"]
    put_prices = data["Put_prices"]
    weights = data["weightage"]
    weights = tuple(zip(weights.index, weights["Weights"]))

    stock_symbols = daily_prices.columns[1:]

    return expiry_dates, daily_prices, futures_prices, strike_prices, call_prices, put_prices, stock_symbols, weights


def create_instrument_list():
    pass


def calculate_implied_vols(option_price, futures_price, strike_price, time_to_expiry, flag,
                           risk_free_interest_rate=0.06):

    implied_vol=black_model_iv.implied_volatility_of_undiscounted_option_price(option_price,futures_price,
                                                                               strike_price,time_to_expiry,flag)

    return implied_vol

def calculate_basket_implied_vols():
    pass


def calculate_dirty_correlation():
    pass


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    current_folder_path = Path().absolute().joinpath("vol_arb")
    input_file_path = current_folder_path / "vol_arb_pricing.xlsx"

    expiry_dates, daily_prices, futures_prices, \
    strike_prices, call_prices, put_prices, stock_symbols, \
    weights = import_data(input_file_path)

    current_expiry=expiry_dates.index.to_series()
    next_expiry=pd.to_datetime(expiry_dates["next_expiry_date"])

    expiry_dates["time_to_expiry"]=(next_expiry-current_expiry)
    expiry_dates["time_to_expiry"]=expiry_dates["time_to_expiry"].apply(lambda x:x.days/365)

    implied_vols_calls = pd.DataFrame()
    implied_vols_puts = pd.DataFrame()

    for stock in stock_symbols:
        for expiry_date in call_prices.index:

            if expiry_date==call_prices.index[-2]:
                print("stop")

            call_premium = call_prices.at[expiry_date,stock]
            put_premium = put_prices.at[expiry_date,stock]
            underlying_price = daily_prices.at[expiry_date,stock]
            futures_price=futures_prices.at[expiry_date,stock]
            strike_price = strike_prices.at[expiry_date,stock]
            expiry_dt = expiry_dates.at[expiry_date,"next_expiry_date"]
            time_to_expiry=expiry_dates.at[expiry_date,"time_to_expiry"]
            risk_free_interest_rate = 0.06
            implied_vols_calls.at[expiry_date,stock] = calculate_implied_vols \
                (call_premium, futures_price, strike_price, time_to_expiry, "c", risk_free_interest_rate)

            implied_vols_puts.at[expiry_date,stock] = calculate_implied_vols \
                (put_premium, futures_price, strike_price, time_to_expiry, "p", risk_free_interest_rate)

            print(expiry_date)
    pass