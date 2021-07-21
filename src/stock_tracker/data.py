#!/usr/bin/env python3
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


def score(df):
    score = 0
    # 1
    score += df["earningsQuarterlyGrowth"]
    # 2
    score += df["revenueQuarterlyGrowth"]
    # 3
    score += (df["pegRatio"] - 1)
    # 4
    score += (df["grossMargins"] - 0.35)
    # 5
    score -= (df["debtToEquity"] / 100 - 0.35)
    # 7
    score += (df["trailingPE"] / df["forwardPE"])
    return score
