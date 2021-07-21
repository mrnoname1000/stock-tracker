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

    info_keys = [
        "earningsQuarterlyGrowth",
        "revenueQuarterlyGrowth",
        "pegRatio",
        "grossMargins",
        "debtToEquity",
        "ebitda",
        "trailingPE",
        "forwardPE",
    ]
    columns = info_keys + []
    df = pd.DataFrame(columns=columns)

    for ticker in tickers:
        df.loc[ticker.ticker] = [
            ticker.info[key] if key in ticker.info else np.nan
            for key in info_keys
        ]

    df["score"] = data.score(df)

    df.sort_values("score", inplace=True, ascending=False)

    print(df)

    return 0
