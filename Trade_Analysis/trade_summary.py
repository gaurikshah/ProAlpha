import pandas as pd


def trade_summary(trades):
    trade_data = trade_data_table(trades)

    trade_summary_table = []
    all_trade_details = trade_summary_details(trade_data)
    profitable_trade_details = trade_summary_details(trade_data[trade_data["Profitable"]])
    losing_trade_details = trade_summary_details(trade_data[~trade_data["Profitable"]])
    long_trade_details = trade_summary_details(trade_data[trade_data["Trade Position"] == 1])
    short_trade_details = trade_summary_details(trade_data[trade_data["Trade Position"] == -1])

    trade_summary_table.append(all_trade_details)
    trade_summary_table.append(profitable_trade_details)
    trade_summary_table.append(losing_trade_details)
    trade_summary_table.append(long_trade_details)
    trade_summary_table.append(short_trade_details)

    trade_summary_table = pd.DataFrame(trade_summary_table)

    trade_summary_table.columns = ["Total Trades", "Profit Factor", "Total Profit", "Average Profit", "Max Profit",
                                   "Min Profit", "Average Duration", "Hit Ratio", "Profitability", "Max DD in Trade",
                                   "Max Profit in Trade", "Max Loss in Trade", "Max Recovery in Trade",
                                   "Max DD Duration in Trade"]
    trade_summary_table["Trades"] = ["ALL Trades", "Profitable Trades", "Losing Trades", "Long Trades", "Short Trades"]
    trade_summary_table.set_index("Trades", inplace=True)

    return trade_summary_table


def trade_summary_details(trade_data):
    no_of_trades = len(trade_data.index)
    if no_of_trades == 0:

        no_trades=[0]*14
        return no_trades

    total_profit = trade_data["Trade Pnl"].sum()
    average_profit = trade_data["Trade Pnl"].mean()
    max_profit = trade_data["Trade Pnl"].max()
    min_profit = trade_data["Trade Pnl"].min()
    average_duration = trade_data["Trade Duration"].mean()
    hit_ratio = len(trade_data[trade_data["Profitable"]].index) / len(trade_data.index)
    profitability = -1 * (trade_data[trade_data["Profitable"]]["Trade Pnl"].mean()) / (
        trade_data[~trade_data["Profitable"]]["Trade Pnl"].mean())
    profit_factor = -1*(trade_data[trade_data["Profitable"]]["Trade Pnl"].sum()) / (
        trade_data[~trade_data["Profitable"]]["Trade Pnl"].sum())
    max_DD_in_trade = trade_data["Max DD"].min()
    max_profit_in_trade = trade_data["Max Profit"].max()
    max_loss_in_trade = trade_data["Max Loss"].min()
    max_recovery_in_trade = trade_data["Max Recovery"].max()
    max_DD_duration_in_trade = trade_data["Max DD Duration"].max()

    return no_of_trades, profit_factor, total_profit, average_profit, max_profit, min_profit, average_duration, \
           hit_ratio, profitability, max_DD_in_trade, max_profit_in_trade, max_loss_in_trade, max_recovery_in_trade, \
           max_DD_duration_in_trade


def trade_data_table(trades):

    trade_data = pd.DataFrame.from_records([x.get_trade_data() for x in trades], index="Trade Number")

    return trade_data
