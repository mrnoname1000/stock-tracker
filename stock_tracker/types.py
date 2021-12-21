import pandas as pd
import yfinance as yf

from . import yahoo
from .yahoo import YahooEarningsCalendar


EARNINGS_CONSTANT_KEYS = [
    "ticker",
    "companyshortname",
]


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
