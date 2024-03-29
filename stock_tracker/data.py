from math import inf

import numpy as np
import pandas as pd


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

    if prices.empty:
        return False

    prices = prices.asfreq("15D", method="pad")

    prices.index.sort_values()

    close = prices["Close"]

    mean = close.rolling(window=len(close)).mean().iloc[-1]
    stddev = close.std()

    plus_sigma = mean + stddev
    minus_sigma = mean - stddev


    # more filters
    # TODO: Weight this one
    mcap = stock.info.get("marketCap", inf)
    if mcap < 10 ** 9:
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

    roe = stock.info.get("returnOnEquity", inf)
    if roe < 0.2:
        return False

    if stock.info.get("debtToEquity", 0) > 50:
        return False

    if stock.info.get("profitMargins", 0) < 0.2:
        return False

    if stock.info.get("grossMargins", 0) < 0.35:
        return False


    return True
