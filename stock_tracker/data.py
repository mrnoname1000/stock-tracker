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


    # Calculate positive/negative sigma
    prices = stock.history(period="3mo", interval="1d")
    prices = prices.asfreq("15D", method="pad")

    prices.index.sort_values()

    close = prices["Close"]

    mean = close.rolling(window=len(close)).mean().iloc[-1]
    stddev = close.std()

    plus_sigma = mean + stddev
    minus_sigma = mean - stddev


    # more filters
    # TODO: Weight this one
    if stock.info["marketCap"] < 10 ** 9:
        return False

    # TODO: check if volume is 10-day average
    if stock.info["volume"] < 150000:
        return False

    trailingpe = stock.info.get("trailingPE")
    if trailingpe is None:
        trailingpe = stock.info["currentPrice"] / stock.info["trailingEps"]

    if trailingpe > 25:
        return False

    if stock.info.get("forwardPE", 0) > 20:
        return False

    if stock.info.get("returnOnEquity", 0) < 0.2:
        return False

    if stock.info.get("debtToEquity", 0) > 50:
        return False

    if stock.info.get("profitMargins", 0) < 0.2:
        return False

    if stock.info.get("grossMargins", 0) < 0.35:
        return False


    return True
