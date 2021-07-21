import textwrap
import math

import numpy as np
import pandas as pd

from . import option, data, yfinance as yf


def main():
    opts = option.build_parser().parse_args()

    if not opts.stocks:
        opts.lookup = True

    if opts.lookup:
        from get_all_tickers import get_tickers as gt

        opts.stocks += gt.get_tickers_filtered(
            mktcap_min=opts.market_cap_min,
            mktcap_max=opts.market_cap_max,
        )

    tickers = yf.Tickers(opts.stocks).tickers.values()

    # stock analysis
    columns = [
        "earningsQuarterlyGrowth",
        "revenueQuarterlyGrowth",
    ]
    df = pd.DataFrame(columns=columns)

    for ticker in tickers:
        df.loc[ticker.ticker] = [
            ticker.info["earningsQuarterlyGrowth"],
            # revenueGrowth seems to be quarterly revenue growth
            ticker.info["revenueGrowth"],
        ]

    df["Rank"] = (
        df[columns]
        .apply(tuple, axis=1)
        .rank(method="dense", ascending=False)
        .astype(int)
    )
    df.sort_values("Rank", inplace=True, ascending=False)

    print(df)

    return 0
