#!/usr/bin/env python3
import numpy as np

def obv(ticker, period="1mo"):
    """
    Calculate OBV for a stock

    Arguments:
        ticker: yfinance Ticker object
        period: any period accepted by yfinance.history()

    Return:
        an integer
    """
    df = ticker.history(period=period)
    if len(df.index) <= 1:
        return 0

    return (np.sign(df["Close"].diff()) * df["Volume"]).cumsum().values[-1]
