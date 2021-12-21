import pandas as pd
import yfinance as yf

from datetime import timedelta
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


def get_stocks_with_earnings_between(start, end):
    yec = YahooEarningsCalendar()

    return [e["ticker"] for e in yec.earnings_between(start, end)]
