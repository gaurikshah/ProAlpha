from Trade_Analysis import trade_summary
from Timeframe_Manipulation import series_resampling as tm
from Trades import Trades
import pandas as pd


def rolling_12m_trade_summary(trades, price_data):
    price_monthly = tm.price_series_to_month(price_data)
    trade_summary_data = []

    for i in range(len(price_monthly) - 12):

        start_date = price_monthly.index[i]
        start_price = price_monthly["Close"].iloc[i]
        end_date = price_monthly.index[i + 12]
        end_price = price_monthly["Close"].iloc[i + 12]

        selected_trades = list(filter(lambda x: (x.exit_date > start_date and x.entry_date < end_date), trades))
        if len(selected_trades) == 0:
            trade_summary_data.append([0]*14)
            continue
        if selected_trades[0].entry_date < start_date:
            trade_to_replace = selected_trades[0]
            selected_trades[0] = Trades(start_date, start_price, trade_to_replace.exit_date,
                                        trade_to_replace.exit_price, trade_to_replace.trade_position,
                                        price_data.loc[(start_date <= price_data.index) &
                                                       (price_data.index <= trade_to_replace.exit_date)])
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
    trade_summary_data["Months"] = price_monthly.index[12:].strftime("%b-%Y")
    trade_summary_data.set_index("Months", inplace=True)

    return trade_summary_data
