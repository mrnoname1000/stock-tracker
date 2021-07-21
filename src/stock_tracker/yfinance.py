import yfinance as yf


class Ticker(yf.Ticker):
    def get_info(self, proxy=None, as_dict=False, *kargs, **kwargs):
        if not self._fundamentals:
            super()._get_fundamentals()

            # revenueGrowth seems to be quarterly, and revenueQuarterlyGrowth
            # seems to always be None, so swap them
            self._info["revenueQuarterlyGrowth"], self._info["revenueGrowth"] = (
                self._info["revenueGrowth"],
                self._info["revenueQuarterlyGrowth"],
            )
        return super().get_info()


class Tickers(yf.Tickers):
    def __init__(self, tickers):
        tickers = (
            tickers if isinstance(tickers, list) else tickers.replace(",", " ").split()
        )
        self.symbols = [ticker.upper() for ticker in tickers]
        ticker_objects = {}

        for ticker in self.symbols:
            ticker_objects[ticker] = Ticker(ticker)

        self.tickers = ticker_objects
