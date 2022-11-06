"""Do all the batch work here"""

import logging
import os

from constants import months, banks
from addHeader import formatters

old_2022_dir = ""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _getMonth(fileName):
    """
    get a month number from file name
    :param fileName:
    :return: two digit number integer
    """
    fileName = fileName.lower()
    for i, month in enumerate(months):
        if month.lower() in fileName or month.lower()[0:3] in fileName:
            return(int(f"{i+1:02}"))


def _getBank(fileName):
    """
    get bank name
    :param fileName:
    :return:
    """
    fileName = fileName.lower()
    for bank in banks:
        if bank.lower() in fileName:
            return bank
    if "5646" in fileName:
        return "amazon"


def runner(dir):
    for file in os.listdir(dir):
        filePath = os.path.join(dir, file)

        month = _getMonth(file)
        bank = _getBank(file)
        logger.debug(f"{file}: {month}")
        if not (bank and month):
            continue
        logger.debug(f"Formatting {month} {bank}")
        _formatter = formatters.get_formatter(bank)
        formatter = _formatter(
            filepath=filePath,
            bank=bank,
            month=month,
            year="2022",
        )

        formatter.write()
