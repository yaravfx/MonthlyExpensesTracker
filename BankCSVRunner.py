"""
Author: Yara
Date: 2022-10-09
Desc: A command-line tool to read csv-file from bank,
then write a formatted csv with unified header
"""


import argparse
import logging
import os
import pandas as pd
import sys


from formatter import formatters
from batchRunner import runner
import constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    print("ExpensesRunner Running!")
    parser = argparse.ArgumentParser(
        prog="ExpensesRunner",
        description="My very own automatic credit card expenses analysis",
    )
    parser.add_argument(
        "--batch",
        required=False,
        default=False,
        action="store_true",
        help="batch running on all the files in the directory of inputPath"
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

    parser.add_argument(
        "-r",
        "--readMode",
        required=False,
        default=False,
        action="store_true",
        help="Trigger Read mode"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.batch:
        _dir = os.path.dirname(args.inputPath)
        runner(_dir)
        print("Batch runner done.")
        sys.exit(0)

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

        if not args.readMode:
            formatter.write()

        exportFile = formatter.exportFile
        # print(exportFile)

        if args.readMode and not os.path.isfile(exportFile):
            f"{exportFile} doesn't exist yet, can't run read mode."
            sys.exit(1)


        print("Sums:")
        rawData = pd.read_csv(exportFile, sep=",")
        totalExpenses = rawData[["Debit"]].sum()
        # print(f"Total Expanses of {constants.months[int(args.month - 1)]}: {totalExpenses}")
        print(totalExpenses)

        print("Categorize expenses now...")



