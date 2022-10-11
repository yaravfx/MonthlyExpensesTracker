import os

from constants import months, banks
from addHeader import formatters

old_2022_dir = ""



def _getMonth(fileName):
    """
    get a month number from file name
    :param fileName:
    :return: two digit number integer
    """
    fileName = fileName.lower()
    for i, month in enumerate(months):
        if month.lower() in fileName or month.lower()[0:2] in fileName:
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
            # print(True)
            return bank
    return "amazon"

#
for file in os.listdir(old_2022_dir):
    filePath = os.path.join(old_2022_dir, file)

    month = _getMonth(file)
    bank = _getBank(file)
    _formatter = formatters.get_formatter(bank)
    formatter = _formatter(
        filepath=filePath,
        bank=bank,
        month=month,
        year="2022",
    )

    formatter.write()
