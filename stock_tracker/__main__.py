import sys
import pandas as pd

from . import option, data, yahoo


def main():
    opts = option.build_parser().parse_args()

    # pandas config
    pd.set_option("display.float_format", lambda x: f"{x:f}")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)


    stocks = [yahoo.Stock(s) for s in yahoo.get_stocks_with_earnings_between(opts.start, opts.end)]

    for stock in stocks:
        if data.evaluate(stock):
            print(stock.ticker)

    return 0

if __name__ == "__main__":
    sys.exit(main())
