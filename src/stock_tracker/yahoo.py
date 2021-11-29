import sys

import pandas as pd
import yfinance as yf

from contextlib import suppress
from yahoo_earnings_calendar import YahooEarningsCalendar

from . import threading

def get_stock_earnings_data_between(start, end):
    data = pd.DataFrame()

    # fetch yahoo earnings calendar
    yec = YahooEarningsCalendar()
    earnings_reports = yec.earnings_between(start, end)

    for report in earnings_reports:
        del report["gmtOffsetMilliSeconds"]

        ticker = report.pop("ticker")
        df = pd.DataFrame(index=[ticker], data=report)
        data = pd.concat([data, df])

    return data

def get_stock_data(*symbols):
    data = pd.DataFrame()

    def get_ticker(symbol):
        symbol = symbol.upper()

        ticker = yf.Ticker(symbol)
        with suppress(KeyError):
            ticker.get_info()

        return ticker

    # this can take a while, so show a progress bar
    for ticker in threading.thread_map(get_ticker, symbols):
        symbol = ticker.ticker
        info = ticker.info

        # we don't want lists as values
        info = {k: v for k, v in info.items() if not isinstance(v, list)}

        df = pd.DataFrame(index=[symbol], data=info)
        data = pd.concat([data, df])

    return data
