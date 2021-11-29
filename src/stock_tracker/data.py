import numpy as np


def obv(ticker, period="1mo", interval="1d"):
    """
    Calculate OBV for a stock

    Arguments:
        ticker: yfinance Ticker object
        period: same as yfinance.history()
        interval: same as yfinance.history()

    Return:
        an integer
    """
    df = ticker.history(period=period, interval=interval)
    if len(df.index) <= 1:
        return 0

    return (np.sign(df.Close.diff()) * df.Volume).cumsum().values[-1]


def zero_if_nan(x):
    return np.where(np.isnan(x), 0, x)
