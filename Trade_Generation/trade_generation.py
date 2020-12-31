from Trades import Trades


def trade_generation(price_signal,trade_signal="Close"):
    trade_position = 0
    trade_open = False
    trade_number = 0
    entry_date = price_signal.index[0]
    trade = []

    for i in price_signal.index:

        if price_signal.loc[i]["Signal"] != trade_position:
            if not trade_open:
                trade_position = price_signal.loc[i]["Signal"]
                trade_number += 1
                entry_date = i
                trade_open = True
                entry_price = price_signal.loc[i][trade_signal]

            elif 0 == price_signal.loc[i]["Signal"]:
                exit_date = i
                exit_price = price_signal.loc[i][trade_signal]
                trade_a = Trades(entry_date, entry_price, exit_date, exit_price, trade_position, price_signal.loc[
                    (entry_date <= price_signal.index) & (price_signal.index <= exit_date)])
                trade.append(trade_a)
                #print(f"Trade:{trade_number}\n")
                trade_position = 0
                trade_open = False

            else:
                exit_date = i
                exit_price = price_signal.loc[i][trade_signal]
                trade_a = Trades(entry_date, entry_price, exit_date, exit_price, trade_position, price_signal.loc[
                    (entry_date <= price_signal.index) & (price_signal.index <= exit_date)])
                trade.append(trade_a)
                #print(f"Trade:{trade_number}\n")
                trade_position = price_signal.loc[i]["Signal"]
                trade_number = trade_number + 1
                entry_date = i
                entry_price = price_signal.loc[i][trade_signal]
                trade_open = True

    if trade_position != 0:
        exit_date = price_signal.index[-1]
        exit_price = price_signal.iloc[-1]["Close"]
        trade_a = Trades(entry_date, entry_price, exit_date, exit_price, trade_position, price_signal.loc[
            (entry_date <= price_signal.index) & (price_signal.index <= exit_date)])
        trade.append(trade_a)

    return trade
