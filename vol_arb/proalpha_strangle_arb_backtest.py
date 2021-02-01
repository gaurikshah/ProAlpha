import pandas as pd
import numpy as np
import py_vollib.black.implied_volatility as black_model_iv
import py_vollib.black.greeks.analytical as greeks
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

    stock_symbols = daily_prices.columns

    return expiry_dates, daily_prices, futures_prices, strike_prices, call_prices, put_prices, stock_symbols, weights


def create_instrument_list():
    pass


def calculate_implied_vols(option_price, futures_price, strike_price, time_to_expiry, flag,
                           risk_free_interest_rate=0.06):
    implied_vol = black_model_iv.implied_volatility_of_undiscounted_option_price(option_price, futures_price,
                                                                                 strike_price, time_to_expiry, flag)

    return implied_vol


def calculate_delta(futures_price, strike_price, time_to_expiry, flag,
                    risk_free_interest_rate, implied_vol):
    delta = greeks.delta(flag, futures_price, strike_price, time_to_expiry, risk_free_interest_rate,
                         implied_vol)

    return delta


def calculate_basket_implied_vols(implied_vols_call, implied_vols_puts, weights):

    basket_implied_volatility=(implied_vols_call+implied_vols_puts)/2
    basket_implied_volatility=basket_implied_volatility.dot(weights)

    return basket_implied_volatility


def calculate_correlation(index_symbol,stock_basket,weights):

    correl_stocks=pd.DataFrame(columns=stock_basket.columns,index=stock_basket.index)

    for i in stock_basket.columns:
        correl_stocks[i]=index_symbol.rolling(30).corr(stock_basket[i])

    correl_stocks = correl_stocks*weights
    correl_stocks.fillna(0,inplace=True)

    correl=correl_stocks.sum(axis=1)

    return correl

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    current_folder_path = Path().absolute().joinpath("vol_arb")
    input_file_path = current_folder_path / "vol_arb_pricing.xlsx"
    output_file_name="result"

    risk_free_intrest_rate = 0.06
    expiry_dates, daily_prices, futures_prices, \
    strike_prices, call_prices, put_prices, stock_symbols, \
    weights = import_data(input_file_path)

    current_expiry = expiry_dates.index.to_series()
    next_expiry = pd.to_datetime(expiry_dates["next_expiry_date"])

    expiry_dates["time_to_expiry"] = (next_expiry - current_expiry)
    expiry_dates["time_to_expiry"] = expiry_dates["time_to_expiry"].apply(lambda x: x.days / 365)

    implied_vols_calls = pd.DataFrame()
    implied_vols_puts = pd.DataFrame()
    delta_calls = pd.DataFrame()
    delta_puts = pd.DataFrame()
    basket_delta = pd.DataFrame(index=call_prices.index)

    weights_list = map(lambda x: (x[1]), weights)
    weights_list = list(weights_list)

    for stock in stock_symbols:

        for expiry_date in call_prices.index:
            call_premium = call_prices.at[expiry_date, stock]
            put_premium = put_prices.at[expiry_date, stock]
            underlying_price = daily_prices.at[expiry_date, stock]
            futures_price = futures_prices.at[expiry_date, stock]
            strike_price = strike_prices.at[expiry_date, stock]
            expiry_dt = expiry_dates.at[expiry_date, "next_expiry_date"]
            time_to_expiry = expiry_dates.at[expiry_date, "time_to_expiry"]
            risk_free_interest_rate = 0.06
            implied_vols_calls.at[expiry_date, stock] = calculate_implied_vols \
                (call_premium, futures_price, strike_price, time_to_expiry, "c", risk_free_interest_rate)

            implied_vols_puts.at[expiry_date, stock] = calculate_implied_vols \
                (put_premium, futures_price, strike_price, time_to_expiry, "p", risk_free_interest_rate)

            delta_calls.at[expiry_date, stock] = calculate_delta(futures_price, strike_price, time_to_expiry, "c",
                                                                 risk_free_interest_rate,
                                                                 implied_vols_calls.at[expiry_date, stock])
            delta_puts.at[expiry_date, stock] = calculate_delta(futures_price, strike_price, time_to_expiry, "p",
                                                                risk_free_interest_rate,
                                                                implied_vols_puts.at[expiry_date, stock])

    index_symbol = stock_symbols[0]
    combined_delta = delta_calls + delta_puts
    index_delta = combined_delta.pop(index_symbol)
    combined_delta = combined_delta.dot(weights_list)
    net_delta = index_delta + combined_delta

    index_iv = (implied_vols_calls.pop(index_symbol) + implied_vols_puts.pop(index_symbol))/2

    basket_implied_volatility = calculate_basket_implied_vols(implied_vols_calls, implied_vols_puts, weights_list)

    implied_volatility_ratio = index_iv/basket_implied_volatility

    index_prices=daily_prices.pop(index_symbol)

    correl=calculate_correlation(index_prices,daily_prices,weights_list)
    implied_volatility_ratio["correl"]=correl.loc[call_prices.index]
    implied_volatility_ratio["combined_delta"] = combined_delta

    implied_volatility_ratio.name="IV_ratio"
#    combined_delta.name="combined_delta"
    implied_vols_calls.name="IV_calls"
    implied_vols_puts.name="IV_puts"
    delta_calls.name="Call_deltas"
    delta_puts.name="Put_deltas"


    data_frames=[implied_volatility_ratio,implied_vols_calls,implied_vols_puts,delta_calls,delta_puts]


    my_funcs.excel_creation(data_frames, current_folder_path, output_file_name)