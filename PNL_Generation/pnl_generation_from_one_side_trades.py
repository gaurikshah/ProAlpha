import pandas as pd
from Individual_Trades import Individual_Trades
from PNL_Generation import pnl_generation as pg
from Trade_Generation import creating_individual_trade_db
import my_funcs

import warnings



if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    baseamount = 10000000

    price_data = my_funcs.reading_price_data_from_csv()

    trades = my_funcs.reading_trades_from_csv()

    price_data_close = pd.DataFrame(index=price_data.index, columns=["NZ1_Index"])
    price_data_close["NZ1_Index"] = price_data.Close

    trade_register = creating_individual_trade_db.creating_individual_trade_db(trades)

    pnl_series, DD_distribution = pg.pnl_timeseries_multiple_strategy_trade(trade_register, price_data_close,
                                                                            price_data.index, baseamount)

    pnl_series.to_csv("PNL Series New.csv", index=True)

    trade_data = pd.DataFrame.from_records([x.get_individual_trade_data() for x in trade_register], index="Trade ID")
    trade_data.to_csv("Sample Trade Data.csv", index=True)
