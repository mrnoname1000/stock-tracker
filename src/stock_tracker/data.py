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

    return (np.sign(df["Close"].diff()) * df["Volume"]).cumsum().values[-1]


def zero_if_nan(x):
    return np.where(np.isnan(x), 0, x)


def score(df):
    score = 0
    # 1
    score += zero_if_nan(df["earningsQuarterlyGrowth"])
    # 2
    score += zero_if_nan(df["revenueGrowth"])
    # 3
    score += zero_if_nan(df["pegRatio"] - 1)
    # 4
    score += zero_if_nan(df["grossMargins"] - 0.35)
    # 5
    score -= zero_if_nan(df["debtToEquity"] / 100 - 0.35)
    # 7
    score += zero_if_nan(df["trailingPE"]) / df["forwardPE"]

    return score
