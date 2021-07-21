import textwrap
import math
import concurrent.futures

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

    # create cached session
    max_threads = 32
    session = None

    if opts.cache:
        try:
            import requests_cache
        except ImportError:
            pass
        else:
            max_threads = 1
            session = requests_cache.CachedSession(
                "stock-tracker.cache", expire_after=60 * 60
            )

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:

        futures = [
            executor.submit(lambda x: (x.ticker, x.info), ticker) for ticker in tickers
        ]

        for future in futures:
            ticker, info = future.result()

            df.loc[ticker] = [info[key] if key in info else np.nan for key in info_keys]

    df["score"] = data.score(df)

    df.sort_values("score", inplace=True, ascending=False)

    print(df)

    return 0
