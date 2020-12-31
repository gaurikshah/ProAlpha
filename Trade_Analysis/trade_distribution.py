import pandas as pd

import numpy as np

import math


def trade_distribution(trade_data):
    p_50 = trade_data["Trade Pnl"].quantile(q=0.5)
    p_90 = trade_data["Trade Pnl"].quantile(q=0.9)
    p_95 = trade_data["Trade Pnl"].quantile(q=0.95)
    p_99 = trade_data["Trade Pnl"].quantile(q=0.99)

    percentile_data = pd.DataFrame(
        [("50th Percentile", p_50), ("90th percentile", p_90), ("95th Percentile", p_95), ("99th Percentile", p_99)])

    trade_pnl = trade_data["Trade Pnl"]

    a = max(abs(math.ceil(trade_pnl.max() * 10)), abs(math.floor(trade_pnl.min() * 10)))

    bin_values = [a / 10 for a in [*range(-a, a + 1, 1)]]

    freq_dist = np.histogram(trade_pnl, bin_values)

    freq_dist = pd.DataFrame(freq_dist)

    freq_dist.fillna(0, inplace=True)

    return percentile_data, freq_dist
