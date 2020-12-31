from my_funcs import *
import warnings
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import skewnorm



if __name__ == '__main__':

    input_data_folder = Path().absolute().joinpath("Input Data")
    output_folder=Path().absolute().joinpath("Results")

    input_file_path = input_data_folder / "PAYS_simulation_inputs.csv"

    data=pd.read_csv(input_file_path, header=0, index_col=0)

    nifty_calls_cost=0.04
    nifty_puts_cost=0.02
    banknifty_calls_cost=0.05
    banknifty_puts_cost=0.04
    weight_of_nifty=0.5

    stocks_mean= data["Mean"]
    stocks_std = data["Standard_deviation"]

    nifty_weights = data["Nifty_weights"]
    nifty_weights=nifty_weights[nifty_weights>0]
    nifty_stock_std=stocks_std[nifty_weights.index]
    nifty_stock_mean = stocks_mean[nifty_weights.index]


    banknifty_weights=data["BankNifty_weights"]
    banknifty_weights=banknifty_weights[banknifty_weights>0]
    banknifty_stock_std=stocks_std[banknifty_weights.index]
    banknifty_stock_mean = stocks_mean[banknifty_weights.index]

    PAYS_nifty_weights=data["PAYS_Nifty_weights"]
    PAYS_nifty_weights=PAYS_nifty_weights[PAYS_nifty_weights>0]

    PAYS_banknifty_weights = data["PAYS_BankNifty_weights"]
    PAYS_bannifty_weights = PAYS_banknifty_weights[PAYS_banknifty_weights > 0]


    simulation_results=pd.DataFrame(columns=["nifty_returns","PAYS_nifty_stocks_long_returns","PAYS_nifty_call_returns","PAYS_nifty_portfolio_returns",
                                   "banknifty_returns","PAYS_banknifty_stocks_long_returns","PAYS_banknifty_call_returns","PAYS_banknifty_portfolio_returns",
                                   "PAYS_portfolio_returns"])


    for i in range(1,100000):

        if i%10000 ==0:
            print(f"{i} : simulations completed sucessfully")
        stocks_random=np.random.randn(len(stocks_mean))
        stocks_random_returns = (stocks_std* stocks_random) + stocks_mean

        while True:
            try:
                stocks_random_returns.to_csv("random_rets.csv")
                break
            except IOError:
                _=input('file is open, please close the file and press enter')


        nifty_returns=sum(stocks_random_returns[nifty_weights.index] * nifty_weights)
        nifty_puts_returns=max(-nifty_returns,0)-nifty_puts_cost
        PAYS_nifty_stocks_returns=stocks_random_returns[PAYS_nifty_weights.index]
        PAYS_nifty_stocks_long_returns=sum(PAYS_nifty_stocks_returns*PAYS_nifty_weights)
        PAYS_nifty_stocks_returns[PAYS_nifty_stocks_returns>0]=0
        PAYS_nifty_call_returns=sum(PAYS_nifty_stocks_returns*PAYS_nifty_weights)+nifty_calls_cost
        PAYS_nifty_portfolio_returns=PAYS_nifty_call_returns+nifty_puts_returns

        banknifty_returns = sum(stocks_random_returns[banknifty_weights.index] * banknifty_weights)
        banknifty_puts_returns = max(-banknifty_returns, 0) - banknifty_puts_cost
        PAYS_banknifty_stocks_returns = stocks_random_returns[PAYS_banknifty_weights.index]
        PAYS_banknifty_stocks_long_returns = sum(PAYS_banknifty_stocks_returns * PAYS_banknifty_weights)
        PAYS_banknifty_stocks_returns[PAYS_banknifty_stocks_returns > 0] = 0
        PAYS_banknifty_call_returns = sum(PAYS_banknifty_stocks_returns * PAYS_banknifty_weights) + banknifty_calls_cost
        PAYS_banknifty_portfolio_returns = PAYS_banknifty_call_returns + banknifty_puts_returns

        PAYS_portfolio_returns=PAYS_nifty_portfolio_returns*weight_of_nifty+PAYS_banknifty_portfolio_returns*(1-weight_of_nifty)

        simulation_results.loc[i]=[nifty_returns,PAYS_nifty_stocks_long_returns,PAYS_nifty_call_returns,PAYS_nifty_portfolio_returns,
                                   banknifty_returns,PAYS_banknifty_stocks_long_returns,PAYS_banknifty_call_returns,PAYS_banknifty_portfolio_returns,
                                   PAYS_portfolio_returns]

    simulation_results.name = "Simulation_Results"
    to_be_saved_as_excel = [simulation_results]

    excel_creation(to_be_saved_as_excel, output_folder, "Results")
