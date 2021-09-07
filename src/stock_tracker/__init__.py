import numpy as np
import pandas as pd
import yfinance as yf

from contextlib import suppress

from . import constants, option, data, threading


def main():
    opts = option.build_parser().parse_args()


    # pandas config
    pd.set_option("display.float_format", lambda x: f"{x:f}")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)


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


    # get tickers if required
    if not opts.stocks:
        opts.lookup = True

    if opts.lookup:
        from get_all_tickers import get_tickers as gt

        opts.stocks.extend(
            gt.get_tickers_filtered(
                mktcap_min=opts.market_cap_min,
                mktcap_max=opts.market_cap_max,
            )
        )

    # create tickers
    tickers = [yf.Ticker(stock, session=session) for stock in opts.stocks]

    # stock analysis

    # keys that correspond to keys in Ticker.info
    info_keys = [
        "earningsQuarterlyGrowth",
        "revenueGrowth",  # seems to be quarterly
        "pegRatio",
        "grossMargins",
        "debtToEquity",
        "ebitda",
        "trailingPE",
        "forwardPE",
    ]
    columns = info_keys
    df = pd.DataFrame(columns=columns)


    def get_info(x):
        with suppress(KeyError):
            x.get_info()
        return x

    for ticker in threading.thread_map(get_info, tickers):
        if ticker.info is not None:
            df.loc[ticker.ticker] = [
                ticker.info[key] if key in ticker.info else np.nan for key in info_keys
            ]

    df["score"] = data.score(df)

    df.sort_values("score", inplace=True, ascending=False)

    # format for user
    new_columns = {column: column for column in columns}
    new_columns["revenueGrowth"] = "revenueQuarterlyGrowth"

    df.rename(new_columns)
    print(df)

    return 0
