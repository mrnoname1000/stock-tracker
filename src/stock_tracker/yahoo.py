import sys

import pandas as pd
import yfinance as yf

from datetime import datetime, timedelta
from contextlib import suppress
from ratelimit import limits, sleep_and_retry
from tqdm.contrib import tmap
from yahoo_earnings_calendar import YahooEarningsCalendar as _YahooEarningsCalendar

from . import threading


class YahooEarningsCalendar(_YahooEarningsCalendar):
    def __init__(self):
        self.delay = 0

    @sleep_and_retry
    @limits(calls=5, period=1)
    @limits(calls=2000, period=timedelta(hours=1).total_seconds())
    def _get_data_dict(self, url, **headers):
        return super()._get_data_dict(url, **headers)


yec = YahooEarningsCalendar()


def get_stock_earnings_data_between(start, end):
    data = pd.DataFrame()

    # fetch yahoo earnings calendar
    earnings_reports = yec.earnings_between(start, end)

    for report in earnings_reports:
        ticker = report.pop("ticker")
        df = pd.DataFrame(index=[ticker], data=report)
        data = pd.concat([data, df])

    return data

def get_stock_data(*symbols):
    data = pd.DataFrame()

    @sleep_and_retry
    @limits(calls=5, period=1)
    @limits(calls=2000, period=60 * 60)
    def get_ticker(symbol):
        symbol = symbol.upper()

        ticker = yf.Ticker(symbol)
        with suppress(KeyError):
            ticker.get_info()

        return ticker

    # this can take a while, so show a progress bar
    for ticker in tmap(get_ticker, symbols):
        symbol = ticker.ticker
        info = ticker.info

        # we don't want lists as values
        info = {k: v for k, v in info.items() if not isinstance(v, list)}

        df = pd.DataFrame(index=[symbol], data=info)
        data = pd.concat([data, df])

    return data
