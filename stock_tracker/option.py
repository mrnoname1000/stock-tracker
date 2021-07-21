#!/usr/bin/env python3
import sys
import argparse
import textwrap


def period(s):
    """Test for valid time period"""
    lower = s.lower()

    if lower in ("ytd", "max"):
        return s

    for suffix in ("d", "mo", "y"):
        prefix = s[: -len(suffix)]
        if lower.endswith(suffix) and prefix.encode("ascii", errors="replace").isdigit():
            return s

    raise ValueError


INTERVAL_VALUES = (
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
)


def positive_int(i):
    if i < 0:
        raise ValueError
    return int(i)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Rank stocks based on various factors",
    )

    parser.add_argument(
        "stocks",
        metavar="STOCK",
        nargs="*",
        help="Manually specify stocks to search",
    )

    parser.add_argument(
        "--market-cap-min",
        metavar="INT",
        action="store",
        default=50000,
        type=int,
        help="Minimum market cap to search (default: %(default)s)",
    )

    parser.add_argument(
        "--market-cap-max",
        metavar="INT",
        action="store",
        default=None,
        type=positive_int,
        help="Maximum market cap to search (default: %(default)s)",
    )

    parser.add_argument(
        "--period",
        action="store",
        type=period,
        default="1mo",
        help="Period of dates to consider (e.g. 5d, 6mo, 10y, ytd, max) (default: %(default)s)",
    )

    parser.add_argument(
        "--interval",
        action="store",
        choices=INTERVAL_VALUES,
        default="1d",
        help="Granularity of samples (default: %(default)s)",
    )

    parser.add_argument(
        "--lookup",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Look up stocks based on market cap",
    )

    parser.add_argument(
        "--progress",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Show progress bars when fetching data",
    )

    parser.add_argument(
        "--cache",
        action=argparse.BooleanOptionalAction,
        help=argparse.SUPPRESS,
    )

    return parser
