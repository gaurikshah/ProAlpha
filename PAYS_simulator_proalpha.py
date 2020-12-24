from my_funcs import *
import warnings
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import skewnorm



if __name__ == '__main__':

    input_data_folder = Path().absolute().joinpath("Input Data")
    output_folder=Path().absolute().joinpath("Results")

    nifty_weights_file_path = input_data_folder / "Nifty_weights.csv"
    PAYS_weights_file_path = input_data_folder / "PAYS_portfolio_weights.csv"

    nifty_weights_data = pd.read_csv(nifty_weights_file_path, header=0, index_col=0)
    PAYS_weights_data = pd.read_csv(PAYS_weights_file_path, header=0, index_col=0)


    calls_cost=0.0004
    nifty_puts_cost=0.0002

    nifty_weights = nifty_weights_data["Weight"]
    nifty_stocks_mean= nifty_weights_data["Mean"]
    nifty_stocks_std = nifty_weights_data["Standard_deviation"]

    PAYS_weights=PAYS_weights_data["Weight"]
    simulation_results=pd.DataFrame(columns=["Nifty_Returns","Nifty_Puts_Returns","PAYS_call_returns","PAYS_Stocks_returns","PAYS_Portfolio_returns"])


    for i in range(10):
        nifty_stocks_random=np.random.randn(50)
        nifty_stocks_random_returns = (nifty_stocks_std* nifty_stocks_random) + nifty_stocks_mean
        nifty_returns= sum(nifty_stocks_random_returns * nifty_weights)
        nifty_puts_returns=max(-nifty_returns,0)-nifty_puts_cost
        PAYS_stocks_returns=nifty_stocks_random_returns[PAYS_weights.index]
        PAYS_stocks_long_returns=sum(PAYS_stocks_returns*PAYS_weights)
        PAYS_stocks_returns[PAYS_stocks_returns>0]=0
        PAYS_call_returns=sum(PAYS_stocks_returns*PAYS_weights)+calls_cost
        PAYS_portfolio_returns=PAYS_call_returns+nifty_returns
        simulation_results.loc[i]=[nifty_returns,nifty_puts_returns,PAYS_call_returns,PAYS_stocks_long_returns,PAYS_portfolio_returns]

    simulation_results.name = "Simulation_Results"
    to_be_saved_as_excel = [simulation_results]

    excel_creation(to_be_saved_as_excel, output_folder, "Results")
