import datetime as dt
import math



class Individual_Trades:
    trade_register = []
    trade_side_str = {1: "B", -1: "S"}

    def __init__(self, date=dt.date(1000, 1, 1), price=0, side=0, contract="", contract_type="", qty=0,
                 trading_cost=0, strike_price=0):

        self.date = date
        self.price = price
        self.quantity = qty
        self.side = side
        self.contract = contract
        self.contract_type = contract_type
        self.side_str = Individual_Trades.trade_side_str[side]
        self.trading_cost = trading_cost
        self.trading_cost_inr = trading_cost * price * qty
        self.strike_price = strike_price
        self.adjusted_price = self.price * (1 + trading_cost) if self.side == 1 else self.price * (1 - trading_cost)
        self.notional = strike_price * qty if (self.contract_type.upper() in ["C", "P"]) else self.price * self.quantity

        date_str = self.date.strftime("%Y%m%d")

        self.trade_id = f"{contract}_{date_str}_{math.floor(self.price * 100):08}"

        if self.individual_trade_check():
            self.__class__.trade_register.append(self)
        else:
            del self

        Individual_Trades.trade_register = [i for i in Individual_Trades.trade_register if i.quantity != 0]

    def __eq__(self, other):
        return self.trade_id == other.trade_id

    def re_initialise(self):
        Individual_Trades.trade_register=[]

    def get_individual_trade_data(self):
        return {"Trade ID": self.trade_id,
                "Date": self.date,
                "Price": self.price,
                "Quantity": self.quantity,
                "Side": self.side,
                "Buy/Sell": self.side_str,
                "Underlying Contract": self.contract,
                "Underlying Contract Type": self.contract_type,
                "Strike Price": self.strike_price,
                "Trading Cost in percentage": self.trading_cost,
                "Trading Cost in INR": self.trading_cost_inr,
                "Notional": self.notional,
                "Adjusted price": self.adjusted_price
                }

    def individual_trade_check(self):

        for i in Individual_Trades.trade_register:
            if i == self:
                a = i.quantity * i.side + self.quantity * self.side
                i.quantity = abs(a)
                i.side = 1 if a >= 0 else -1
                i.trading_cost_inr = i.quantity * i.trading_cost * i.price
                i.adjusted_price = i.price * (1 + i.trading_cost) if i.side == 1 else i.price * (1 - i.trading_cost)
                i.notional = i.strike_price * i.quantity if (
                        i.contract_type.upper() in ["C", "P"]) else i.price * i.quantity
                i.side_str = Individual_Trades.trade_side_str[i.side]
                return False
        return True
