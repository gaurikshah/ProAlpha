import math
from Position_Sizing import Position_Sizing_Monthly_Rebalance as ps
from PNL_Generation.Drawdown_Calc import *


def pnl_timeseries_same_value_trade(trades, price_data, baseamount):
    current_equity = baseamount
    trade_count = 0
    no_of_trades = len(trades)

    pnl_series = pd.DataFrame(0, index=price_data.index, columns=["PNL", "%PNL", "Equity", "EOD Position", "DD"])

    while trade_count < no_of_trades:
        entry_date = trades[trade_count].entry_date
        exit_date = trades[trade_count].exit_date
        trade_position = trades[trade_count].trade_position
        price_series = trades[trade_count].price_data["Close"]
        entry_price = trades[trade_count].entry_price
        exit_price = trades[trade_count].exit_price
        trade_units = math.floor(current_equity / entry_price)
        price_series[-1] = exit_price

        eq_curve = (trade_units * price_series)
        profit_curve = (eq_curve - current_equity) * trade_position
        daily_profit = profit_curve - profit_curve.shift(1)
        daily_profit[0] = profit_curve[0]

        pnl_series["PNL"].loc[entry_date:exit_date] = pnl_series["PNL"].loc[entry_date:exit_date] + daily_profit

        pnl_series["EOD Position"].loc[entry_date:exit_date] = trade_position

        trade_count += 1

    pnl_series["Equity"] = pnl_series["PNL"].cumsum() + current_equity
    pnl_series["%PNL"] = pnl_series["PNL"] / current_equity

    pnl_series["DD"], DD_distribution = DD_cum(pnl_series["Equity"])

    pnl_series = pnl_series.round({"Equity": 2, "PNL": 2})

    pnl_series.fillna(0, inplace=True)

    return pnl_series, DD_distribution


def pnl_timeseries_monthly_rebalance(trades, price_data, baseamount):
    position_size = ps.position_size(price_data, baseamount)
    trade_count = 0
    no_of_trades = len(trades)
    current_equity = baseamount

    pnl_series = pd.DataFrame(0, index=price_data.index, columns=["PNL", "%PNL", "Equity", "EOD Position", "DD"])

    while trade_count < no_of_trades:
        entry_date = trades[trade_count].entry_date
        exit_date = trades[trade_count].exit_date
        trade_position = trades[trade_count].trade_position
        price_series = trades[trade_count].price_data["Close"]
        entry_price = trades[trade_count].entry_price
        exit_price = trades[trade_count].exit_price
        price_series[-1] = exit_price

        trade_units = position_size[entry_date:exit_date]

        daily_profit = trade_units * (price_series - price_series.shift(1)) * trade_position
        daily_profit[0] = trade_units[0] * (price_series[0] - entry_price) * trade_position

        pnl_series["PNL"].loc[entry_date:exit_date] = pnl_series["PNL"].loc[entry_date:exit_date] + daily_profit

        pnl_series["EOD Position"].loc[entry_date:exit_date] = trade_position
        pnl_series["EOD Position"].loc[exit_date] = 0

        trade_count += 1

    pnl_series["Equity"] = pnl_series["PNL"].cumsum() + current_equity
    pnl_series["%PNL"] = pnl_series["PNL"] / current_equity

    pnl_series["DD"], DD_distribution = DD_sum(pnl_series["Equity"], baseamount)

    pnl_series = pnl_series.round({"Equity": 2, "PNL": 2})

    pnl_series.fillna(0, inplace=True)

    return pnl_series, DD_distribution


def pnl_timeseries_multiple_strategy_trade(trades, price_data, dates, baseamount):
    contract_list = list(price_data.keys())

    position_data = pd.DataFrame(0, index=dates, columns=contract_list)
    pnl_data_trade = pd.DataFrame(0, index=dates, columns=contract_list)
    pnl_data_position = pd.DataFrame(0, index=dates, columns=contract_list)
    pnl_series = pd.DataFrame(0,index=dates,columns=["Daily PNL"])


    price_data_close_series = pd.DataFrame(0, index=dates, columns=contract_list)
    for contract in contract_list:
        price_data_close_series[contract] = price_data[contract]["Close"]

    price_data_close_series.fillna(method="ffill", inplace=True)
    price_data_close_series.fillna(0, inplace=True)
    for i in trades:
        position_data[i.contract].loc[i.date] += i.quantity * i.side
        pnl_data_trade[i.contract].loc[i.date] += (
                    (price_data_close_series[i.contract].loc[i.date] - i.adjusted_price) * i.side * i.quantity)
    position_data = position_data.cumsum()
    position_data.fillna(0)

    gross_exposure_data = position_data.abs() * price_data_close_series
    net_exposure_data = position_data * price_data_close_series

    for contract in contract_list:
        pnl_data_position[contract] = position_data[contract].shift(1) * (
                price_data_close_series[contract] - price_data_close_series[contract].shift(1))

    pnl_series["Daily PNL"] = pnl_data_position.sum(axis=1) + pnl_data_trade.sum(axis=1)
    pnl_series["Gross Exposure"] = gross_exposure_data.sum(axis=1)
    pnl_series["EOD Net Exposure"] = net_exposure_data.sum(axis=1)
    pnl_series["Cumulative PNL"] = pnl_series["Daily PNL"].cumsum()
    pnl_series["Cumulative PNL%"] = pnl_series["Cumulative PNL"] / baseamount
    pnl_series["DD in %"], DD_distribution = DD_sum(pnl_series["Cumulative PNL"], baseamount)
    pnl_series["DD in INR"] = (pnl_series["Cumulative PNL"] - (pnl_series["Cumulative PNL"].shift(1).cummax()))
    # pnl_series["DD in INR"]=pnl_series["DD in INR"].apply(lambda x: [y if y<0 else 0 for y in x])
    pnl_series["DD in INR"][pnl_series["DD in INR"] > 0] = 0
    pnl_series["DD in INR"].fillna(0, inplace=True)

    return pnl_series, DD_distribution
