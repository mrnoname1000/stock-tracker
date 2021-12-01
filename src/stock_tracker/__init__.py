import numpy as np
import pandas as pd
import yfinance as yf

from yahoo_earnings_calendar import YahooEarningsCalendar

from . import constants, option, data, threading, yahoo


def main():
    opts = option.build_parser().parse_args()

    # pandas config
    pd.set_option("display.float_format", lambda x: f"{x:f}")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)


    # get yahoo calendar data
    earnings = yahoo.get_stock_earnings_data_between(opts.start, opts.end)

    for ticker, df in earnings.items():
        yahoo.populate_earnings_df(ticker, df)

        if data.evaluate(df):
            print(ticker, sep="\n")

    return 0
