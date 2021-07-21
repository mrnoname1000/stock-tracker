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

    # stock analysis
    columns = [
        "OBV",
    ]
    df = pd.DataFrame(columns=columns)

    for ticker in tickers:
        df.loc[ticker.ticker] = [
            data.obv(ticker, period=opts.period, interval=opts.interval)
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
