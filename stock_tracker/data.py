import numpy as np
import pandas as pd


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


def evaluate(stock):
    ec = stock.earnings_calendar

    ec.index.sort_values()

    # Ignore future reports
    ec_past = ec.loc[ec["epsactual"].notna()]

    # Ignore brand-new stocks
    if len(ec_past) < 2:
        return False

    # Guarantee MRQ earnings gain of >= 100%
    if 2 * ec_past.iloc[0]["epsactual"] < ec_past.iloc[1]["epsactual"]:
        return False

    return True
