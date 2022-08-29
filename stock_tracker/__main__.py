import sys, traceback
import pandas as pd

from yahoo_earnings_calendar import CalendarError
from . import option, data, yahoo


def main():
    opts = option.build_parser().parse_args()

    # pandas config
    pd.set_option("display.float_format", lambda x: f"{x:f}")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)


    if opts.lookup:
        tickers = yahoo.get_stocks_with_earnings_between(opts.start, opts.end)
    else:
        tickers = opts.stocks
    stocks = [yahoo.Stock(t) for t in tickers]

    for stock in stocks:
        print("Evaluating", stock.ticker)
        try:
            if data.evaluate(stock):
                print(stock.ticker)
        except (KeyError, ValueError, CalendarError, TypeError) as e:
            traceback.print_exc(file=sys.stderr)
            print("Exception caught, continuing...", file=sys.stderr)

    return 0

if __name__ == "__main__":
    sys.exit(main())
