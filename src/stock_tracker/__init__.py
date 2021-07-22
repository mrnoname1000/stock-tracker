import textwrap
import math
import concurrent.futures

import numpy as np
import pandas as pd

from . import constants, option, data, threading, yfinance as yf


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


    # create cached session if requested
    if opts.cache:
        try:
            import requests_cache
        except ImportError:
            pass
        else:
            session = requests_cache.CachedSession(constants.REQUESTS_CACHE, expire_after=60 * 60)
    else:
        session = None

    # create tickers
    tickers = [yf.Ticker(stock, session=session) for stock in opts.stocks]

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


    def get_info(x):
        try:
            info = x.info
        except KeyError as e:
            info = None
        return x.ticker, info

    for ticker, info in threading.thread_map(
        get_info,
        tickers,
        progress=opts.progress,
    ):
        if info is not None:
            df.loc[ticker] = [info[key] if key in info else np.nan for key in info_keys]

    df["score"] = data.score(df)

    df.sort_values("score", inplace=True, ascending=False)

    print(df)

    return 0
