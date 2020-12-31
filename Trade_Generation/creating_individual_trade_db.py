from Individual_Trades import Individual_Trades

def creating_individual_trade_db(trades):

    for i in trades.index:

        a = Individual_Trades(trades.iloc[i].Date,
                              trades.iloc[i].Price,
                              trades.iloc[i].Side,
                              trades.iloc[i].Contract,
                              trades.iloc[i].Contract_Type,
                              trades.iloc[i].Qty,
                              trades.iloc[i].Trading_Cost,
                              trades.iloc[i].Strike_Price)

    trade_register = Individual_Trades.trade_register
    trade_register.sort(key=lambda x: x.date)

    return trade_register
