import csv
from enum import Enum
import logging
import re

import constants

# class Formatter:
FIELDNAMES = ["Date", "Detail", "Debit", "Credit", "Balance", "Category"]

logger = logging.getLogger(__name__)


class HEADER(Enum):
    Date = 1
    Detail = 2
    Debit = 3
    Credit = 4
    Balance = 5
    Category = 6


class bankCsvFromatterFactory:
    def __init__(self):
        self._FORMATTERS = {}

    def register_format(self, bank, formatter):
        self._FORMATTERS[bank] = formatter

    def get_formatter(self, bank):
        formatter = self._FORMATTERS.get(bank)
        if not formatter:
            raise ValueError(bank)
        return formatter


class BankCsvFormatter:
    def __init__(self, filepath, bank, month, year, exportFile):
        self.filepath = filepath
        self.exportFile = exportFile or constants.exportFileFormatter.format(month, year, bank)
        self._copyLines = None

    def addHeader(self):
        return []

    @property
    def copyLines(self):
        if self._copyLines is None:
            self._copyLines = self.addHeader()
        return self._copyLines

    def write(self):
        with open(self.exportFile, "w+", newline="") as new_csvFile:
            fieldnames = FIELDNAMES
            writer = csv.DictWriter(new_csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for line in self.copyLines:
                writer.writerow(line)


class AmazonCreditCardFormatter(BankCsvFormatter):
    def __init__(self, filepath, bank, month, year, exportFile):
        BankCsvFormatter.__init__(self, filepath, bank, month, year, exportFile)

    def addHeader(self):
        with open(self.filepath, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader, None)
            copyLines = []
            for row in reader:
                debit, credit = "", ""
                if float(row[3]) > 0:
                    credit = row[3]
                else:
                    debit = abs(float(row[3]))
                copyLines.append(
                    {
                        HEADER.Date.name: row[0],
                        HEADER.Detail.name: row[1],
                        HEADER.Debit.name: debit,
                        HEADER.Credit.name: credit,
                        HEADER.Balance.name: ""
                    }
                )
        return copyLines


class TangerineCsvFormatter(BankCsvFormatter):
    def __init__(self, filepath, bank, month, year, exportFile):
        BankCsvFormatter.__init__(self, filepath, bank, month, year, exportFile)

    def addHeader(self):
        with open(self.filepath, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader, None)
            copyLines = []
            for row in reader:
                debit, credit, category = "", "", ""
                if float(row[4]) > 0:
                    credit = row[4]
                else:
                    debit = abs(float(row[4]))
                if "Category:" in row[3]:
                    category = re.findall("Category:\s(.*)", row[3])[0]

                copyLines.append(
                    {
                        HEADER.Date.name: row[0],
                        HEADER.Detail.name: row[2],
                        HEADER.Debit.name: debit,
                        HEADER.Credit.name: credit,
                        HEADER.Balance.name: "",
                        HEADER.Category.name: category
                    }
                )
        return copyLines


class TDCsvFormatter(BankCsvFormatter):
    def __init__(self, filepath, bank, month, year, exportFile):
        BankCsvFormatter.__init__(self, filepath, bank, month, year, exportFile)

    def addHeader(self):
        with open(self.filepath, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            copyLines = []
            for row in reader:
                copyLines.append(
                    {
                        HEADER.Date.name: row[0],
                        HEADER.Detail.name: row[1],
                        HEADER.Debit.name: row[2],
                        HEADER.Credit.name: row[3],
                        HEADER.Balance.name: "",
                    }
                )
        return copyLines


formatters = bankCsvFromatterFactory()
formatters.register_format("amazon", AmazonCreditCardFormatter)
formatters.register_format("tangerine", TangerineCsvFormatter)
formatters.register_format("TD", TDCsvFormatter)








