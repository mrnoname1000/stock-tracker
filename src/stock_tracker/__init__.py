import textwrap
import math

import numpy as np
import pandas as pd
import yfinance as yf

from get_all_tickers import get_tickers as gt

from . import option, data


def main():
    parser = option.build_parser()
    opts = parser.parse_args()

    stocks = gt.get_tickers_filtered(
        mktcap_min=opts.market_cap_min,
        mktcap_max=opts.market_cap_max,
    )
    tickers = yf.Tickers(stocks).tickers

    # OBV analysis
    obv_df = pd.DataFrame(columns=["OBV"])

    for stock, df in tickers.items():
        obv_df.loc[stock] = data.obv(df.history(period=opts.period))

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
