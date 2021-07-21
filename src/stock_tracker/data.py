#!/usr/bin/env python3

import numpy as np

def obv(ticker, period="1mo"):
    """
    Calculate OBV for a stock

    Arguments:
        ticker: yfinance Ticker object
        period:

    Return:
        a single integer of the type used by yfinance
    """
    df = ticker.history(period=period)
    return (np.sign(df["Close"].diff()) * df["Volume"]).cumsum().values[-1]
