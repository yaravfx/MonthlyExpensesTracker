"""Analyse formatted csv files and categorize each item in the csv"""

import csv
from enum import Enum
import logging
import re

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filePath = r"C:\Users\kiwif\Dropbox\Personal\Finance\2022_new\09-2022_TD_credit_card.csv"
# with open(filePath, newline="") as csvfile:
#     csvReader = csv.reader(csvfile, delimiter=",")
#     next(csvReader, None)
#     categories = []
#     for row in csvReader:
#         if




rawData = pd.read_csv(filePath)

categoriesI = []
for i in rawData.Detail.tolist():
    i = i.lower()
    categoryI = "Other"
    if "uber" in i:
        categoryI = "Delivery"
    elif any (c in i for c in ("sushi", "ramen", "noodle", "coffee", "cafe", "tea")):
        categoryI = "Eat Out"
    elif any(c in i for c in ("save on foods", "nayax", "supermarket", "safeway", "market", "sungiven foods")):
        categoryI = "Groceries"
    elif any(c in i for c in ("bosley", "pet")):
        categoryI = "Pet Food"
    elif any(c in i for c in ("cognosphere",)):
        categoryI = "Game"
    elif any(c in i for c in ("youtubepremium", "apple.com/bill")):
        categoryI = "Subscription"
    elif any(c in i for c in ("telus", "novus", "koodo")):
        categoryI = "Utilities"

    categoriesI.append(categoryI)
    # print(i, categoryI)
# print(categoriesI)

rawData["CategoryI"] = categoriesI
rawData.to_csv(filePath)

print(type(rawData.groupby("CategoryI")))
print(dir(rawData.groupby("CategoryI")))
print(help(rawData.groupby("CategoryI").sum))
category_sums = rawData.groupby("CategoryI").sum()
print(category_sums)

ax = category_sums.plot.bar(y="Debit")
plt.xticks(rotation=30)
# pie = category_sums.plot.pie(y="Debit")
# pie.legend()

# ax = category_sums["Debit"].plot.pie()
# ax.legend(loc="upper left", bbox_to_anchor=(1.5, 1))

plt.show()

