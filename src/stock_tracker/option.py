#!/usr/bin/env python3
import sys
import argparse
import textwrap

def positive_int(i):
    if i < 0:
        raise ValueError
    return int(i)

def build_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="assess stocks based on various factors",
    )

    parser.add_argument(
        "--market-cap-min",
        action="store",
        default=50000,
        type=int,
        help=textwrap.dedent("""\
            minimum market cap to search
            default: %(default)s
        """),
    )

    parser.add_argument(
        "--market-cap-max",
        action="store",
        default=None,
        type=positive_int,
        help=textwrap.dedent("""\
            maximum market cap to search
            default: none
        """),
    )

    date_values = ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
    def period(string):
        if string not in date_values:
            raise ValueError
        return string

    parser.add_argument(
        "--period",
        action="store",
        default="max",
        type=period,
        help=textwrap.dedent(f"""\
            period of dates to consider
            valid periods: {', '.join(date_values)}
            default: %(default)s
        """),
    )

    return parser
