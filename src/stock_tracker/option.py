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
        if (
            lower.endswith(suffix)
            and prefix.encode("ascii", errors="replace").isdigit()
        ):
            return s

    raise ValueError


def positive_int(i):
    if i < 0:
        raise ValueError
    return int(i)


def build_parser():
    # TODO: create custom help formatter
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
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
        help=textwrap.dedent(
            """
            Minimum market cap to search
            default: %(default)s
            """
        ).strip("\n"),
    )

    parser.add_argument(
        "--market-cap-max",
        metavar="INT",
        action="store",
        default=None,
        type=positive_int,
        help=textwrap.dedent(
            """
            Maximum market cap to search
            default: none
            """
        ).strip("\n"),
    )

    parser.add_argument(
        "--period",
        action="store",
        type=period,
        default="1mo",
        help=textwrap.dedent(
            f"""
            Period of dates to consider (e.g. 5d, 6mo, 10y, ytd, max)
            default: %(default)s
            """
        ).strip("\n"),
    )

    parser.add_argument(
        "--lookup",
        action=argparse.BooleanOptionalAction,
        help=textwrap.dedent(
            """
            Look up stocks based on market cap
            default: no (unless no stocks are specified)
            """
        ).strip("\n"),
    )

    parser.add_argument(
        "--cache",
        action=argparse.BooleanOptionalAction,
        help=argparse.SUPPRESS,
    )

    return parser
