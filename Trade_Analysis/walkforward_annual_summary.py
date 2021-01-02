import pandas as pd

from Trade_Analysis import trade_summary
from Trades import Trades
from Timeframe_Manipulation import series_resampling as tm


def walkforward_trade_summary(trades, price_data):
    price_annual = tm.price_series_to_annual(price_data)
    trade_summary_data = []

    for i in range(len(price_annual) - 1):

        i = i + 1

        end_date = price_annual.index[i]
        end_price = price_annual["Close"].iloc[i]

        selected_trades = list(filter(lambda x: (x.entry_date < end_date), trades))
        if len(selected_trades) == 0:
            trade_summary_data.append([0] * 5)
            continue

        if selected_trades[-1].exit_date > end_date:
            trade_to_replace = selected_trades[-1]
            selected_trades[-1] = Trades(trade_to_replace.entry_date, trade_to_replace.entry_price, end_date, end_price
                                         , trade_to_replace.trade_position,
                                         price_data.loc[(trade_to_replace.entry_date <= price_data.index) &
                                                        (price_data.index <= end_date)])

        td_summary = trade_summary.trade_summary(selected_trades).iloc[0]

        trade_summary_data.append(td_summary)

    trade_summary_data = pd.DataFrame(trade_summary_data)
    trade_summary_data.columns = ["Total Trades", "Profit Factor", "Total Profit", "Average Profit", "Max Profit",
                                  "Min Profit", "Average Duration", "Hit Ratio", "Profitability", "Max DD in Trade",
                                  "Max Profit in Trade", "Max Loss in Trade", "Max Recovery in Trade",
                                  "Max DD Duration in Trade"]
    trade_summary_data["Years"] = price_annual.index[1:].year
    trade_summary_data.set_index("Years", inplace=True)

    return trade_summary_data
