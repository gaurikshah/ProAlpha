
logic = {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}


def cum_prod(data, last_row=False):
    df = ((1 + data).cumprod(axis=0) - 1)
    if last_row:
        return df.iloc[-1]
    return df


def price_series_periodic(price_data,period="M"):

    price_periodic = price_data.resample(period).apply(logic)

    price_data["Date"]=price_data.index

    idx = price_data.reset_index().groupby(price_data.index.to_period(period))['Date'].idxmax()
    price_periodic.index = price_data.iloc[idx].index

    price_data.drop(["Date"],axis=1,inplace=True)

    return price_periodic


def price_series_to_month(price_data):
    price_monthly = price_data.resample("M").apply(logic)

    return price_monthly


def price_series_to_annual(price_data):

    price_annual = price_data.resample("Y").apply(logic)

    return price_annual


def returns_to_month(returns_data, last_row=True):
    returns_monthly = returns_data.resample("M").apply(cum_prod, last_row)

    return returns_monthly


def returns_to_annual(returns_data, last_row=True):
    returns_annual = returns_data.resample("Y").apply(cum_prod, last_row)

    return returns_annual
