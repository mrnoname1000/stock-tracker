import argparse, datetime


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
        "--lookup",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Look up stocks based on earnings date",
    )

    parser.add_argument(
        "-j",
        "--jobs",
        type=positive_int,
        help="Number of jobs to run in parallel",
    )

    def date(s):
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()

    # TODO: parse time delta on command line
    parser.add_argument(
        "--start",
        type=date,
        metavar="YYYY-MM-DD",
        default=datetime.date.today(),
        help="Start date of earnings reports",
    )

    parser.add_argument(
        "--end",
        type=date,
        metavar="YYYY-MM-DD",
        default=datetime.date.today() + datetime.timedelta(days=90),
        help="End date of earnings reports",
    )

    return parser
