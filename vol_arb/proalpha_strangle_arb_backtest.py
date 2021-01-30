import pandas as pd
import numpy as np
import vollib.black_scholes as black_scholes_model
import warnings
from pathlib import Path
import my_funcs


def import_data(input_file_path):
    data = my_funcs.read_from_excel(input_file_path)

    expiry_dates = data["Expiry"].index
    daily_prices = data["Daily_prices"]
    futures_prices = data["Futures_prices"]
    strike_prices = data["Strike_prices"]
    call_prices = data["Call_prices"]
    put_prices = data["Put_prices"]
    weights = data["weightage"]
    weights = tuple(zip(weights.index, weights["Weights"]))

    stock_symbols = daily_prices.columns[1:]

    return expiry_dates, daily_prices, futures_prices, strike_prices, call_prices, put_prices, stock_symbols, weights

def calculate_time_to_expiry(current_date,expiry_date):
    time_to_expiry=(expiry_date-current_date)/365

    return time_to_expiry


def create_instrument_list():
    pass


def calculate_implied_vols(option_price, futures_price, strike_price, dt, expiry_dt, flag,
                           risk_free_interest_rate=0.06):
    pass



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

    expiry_dates["Time_toExpiry"]=(expiry_dates["next_expiry_date"]-expiry_dates.index)/365

    implied_vols_calls = pd.DataFrame()
    implied_vols_puts = pd.DataFrame()

    for stock in stock_symbols:
        for expiry_date in call_prices.index:
            call_premium = call_prices[stock].iloc[expiry_date]
            put_premium = put_prices[stock].iloc[expiry_date]
            futures_price = futures_prices[stock].iloc[expiry_date]
            strike_price = strike_prices[stock].iloc[expiry_date]
            expiry_dt = expiry_dates["next_expiry_date"].iloc[expiry_date]
            risk_free_interest_rate = 0.06
            implied_vols_calls[stock].iloc[expiry_date] = calculate_implied_vols \
                (call_premium, futures_price, strike_price, expiry_date, expiry_dt, "C", risk_free_interest_rate)

            implied_vols_puts[stock].iloc[expiry_date] = calculate_implied_vols \
                (put_premium, futures_price, strike_price, expiry_date, expiry_dt, "P", risk_free_interest_rate)

    pass
