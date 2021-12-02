import argparse, parsedatetime


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

    cal = parsedatetime.Calendar()
    def date(s, cal=cal):
        date_obj, parse_status = cal.parseDT(s)
        if parse_status == 0:
            raise ValueError
        return date_obj.date()

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
