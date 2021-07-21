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

    if not opts.stocks:
        opts.stocks = gt.get_tickers_filtered(
            mktcap_min=opts.market_cap_min,
            mktcap_max=opts.market_cap_max,
        )
    tickers = yf.Tickers(opts.stocks).tickers.values()

    # OBV analysis
    obv_df = pd.DataFrame(columns=["OBV"])

    for ticker in tickers:
        obv_df.loc[ticker.ticker] = data.obv(ticker.history(period=opts.period))

    obv_df["Rank"] = obv_df["OBV"].rank(ascending=False)
    obv_df.sort_values("OBV", inplace=True, ascending=False)


    print(obv_df)

    return 0
