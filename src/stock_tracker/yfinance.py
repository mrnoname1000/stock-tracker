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
