import textwrap
import math
import concurrent.futures

import numpy as np
import pandas as pd

from . import option, data, threading, yfinance as yf


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
    max_threads = 32
    session = None

    if opts.cache:
        try:
            import requests_cache
        except ImportError:
            pass
        else:
            max_threads = 1
            session = requests_cache.CachedSession("stock-tracker.cache", expire_after=60 * 60)

    # create tickers
    tickers = yf.Tickers(opts.stocks, session=session).tickers.values()

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

    threads = min(max_threads, len(tickers))
    for ticker, info in threading.tmap(
        lambda x: (x.ticker, x.info),
        tickers,
        max_workers=threads,
        progress=opts.progress,
    ):
        df.loc[ticker] = [info[key] if key in info else np.nan for key in info_keys]

    df["score"] = data.score(df)

    df.sort_values("score", inplace=True, ascending=False)

    print(df)

    return 0
