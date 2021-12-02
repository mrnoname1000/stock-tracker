import argparse, dateparser, re


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

    dateparser_settings = {
        "PREFER_DAY_OF_MONTH": "first",
    }
    def date(s, settings=dateparser_settings):
        # dateparser parses plus as minus for some reason
        s = re.sub(r"[+]", " in ", s)
        return dateparser.parse(s, settings=settings)

    parser.add_argument(
        "--start",
        type=date,
        metavar="TIMESPEC",
        default="+45days",
        help="Start date of earnings reports",
    )

    parser.add_argument(
        "--end",
        type=date,
        metavar="TIMESPEC",
        default="+90days",
        help="End date of earnings reports",
    )

    return parser
