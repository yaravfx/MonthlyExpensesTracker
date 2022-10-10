"""
Author: Yara
Date: 2022-10-09
Desc: Automatic Credit Card Expenses Analysis
"""


import argparse
import logging
import sys
import os

from addHeader import formatters
import constants


if __name__ == "__main__":
    print("ExpensesRunner Running!")
    parser = argparse.ArgumentParser(
        prog="ExpensesRunner",
        description="My very own automatic credit card expenses analysis",
    )

    parser.add_argument(
        "-i",
        "--inputPath",
        type=str,
        help="Bank website downloaded credit card transaction csv file",
    )

    parser.add_argument(
        "-b", "--bank", type=str, help="Bank name: TD, amazon, tangerine"
    )

    parser.add_argument(
        "-m", "--month", type=int, help="Month of the transaction in digit"
    )

    parser.add_argument(
        "-y", "--year", default=2022, type=int, help="Year of the transaction in digit"
    )

    parser.add_argument(
        "-e",
        "--export",
        required=False,
        type=str,
        help="Export file path",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    try:
        _formatter = formatters.get_formatter(args.bank)
    except ValueError:
        print(f"Bank {args.bank} is not supported")
        sys.exit(1)
    else:
        print(f"Running {_formatter}")
        formatter = _formatter(
            filepath=args.inputPath,
            bank=args.bank,
            month=args.month,
            year=args.year,
            exportFile=args.export,
        )
        formatter.write()
