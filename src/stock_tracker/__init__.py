import textwrap
import math

import numpy as np
import pandas as pd
import yfinance as yf

from get_all_tickers import get_tickers as gt

def main():
    stocks = gt.get_tickers_filtered(mktcap_min=50000)
    tickers = yf.Tickers(stocks).tickers
    histories = {stock: ticker.history(period="max") for stock, ticker in tickers.items()}

    # OBV analysis
    obv_df = pd.DataFrame(columns=["OBV"])

    for stock, df in histories.items():
        obv = (np.sign(df["Close"].diff()) * df["Volume"]).cumsum().to_numpy()[-1]
        obv_df.loc[stock] = obv

    obv_df["Rank"] = obv_df["OBV"].rank(ascending=False)
    obv_df.sort_values("OBV", inplace=True, ascending=False)

    cutcount = min(10, len(obv_df.index) / 2)
    print(textwrap.dedent(f"""
        Subject: Daily Stock Report

        Your highest ranked OBV stocks of the day:

        {' '.join(obv_df.head(math.ceil(cutcount)).index.values)}

        Your lowest ranked OBV stocks of the day:

        {' '.join(obv_df.tail(math.floor(cutcount)).index.values[::-1])}

        Sincerely,
        Your Computer
    """.strip("\n")))

    return 0
