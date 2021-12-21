import pandas as pd
import yfinance as yf

from datetime import timedelta
from contextlib import suppress
from ratelimit import limits, sleep_and_retry
from tqdm.contrib import tmap
from yahoo_earnings_calendar import YahooEarningsCalendar as _YahooEarningsCalendar

from . import threading


EARNINGS_CONSTANT_KEYS = [
    "ticker",
    "companyshortname",
]


class YahooEarningsCalendar(_YahooEarningsCalendar):
    def __init__(self):
        self.delay = 0

    @sleep_and_retry
    @limits(calls=5, period=1)
    @limits(calls=2000, period=timedelta(hours=1).total_seconds())
    def _get_data_dict(self, url, **headers):
        return super()._get_data_dict(url, **headers)


# yfinance Ticker but with earnings calendar
class Stock(yf.Ticker):
    def __init__(self, ticker, session=None):
        super().__init__(ticker, session)

        self._yec = YahooEarningsCalendar()
        self._earnings_calendar = None


    def _trim_constants(self, earnings_report, constants=EARNINGS_CONSTANT_KEYS):
        for key in constants:
            if key in earnings_report:
                del earnings_report[key]


    def get_earnings_calendar(self):
        if self._earnings_calendar is None:
            ec = self._yec.get_earnings_of(self.ticker)
            for e in ec:
                self._trim_constants(e)
            dates = [e.pop("startdatetime") for e in ec]

            self._earnings_calendar = pd.DataFrame(ec, index=dates)

        return self._earnings_calendar


    @property
    def earnings_calendar(self):
        return self.get_earnings_calendar()


def get_stocks_with_earnings_between(start, end):
    yec = YahooEarningsCalendar()

    return [e["ticker"] for e in yec.earnings_between(start, end)]
