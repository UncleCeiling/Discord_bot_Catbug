from multiprocessing.reduction import duplicate
import os,csv

os.chdir(os.path.dirname(__file__))
file = "adjectives.csv"

with open(file,encoding="utf8") as file:
        items = []
        for line in file.readlines():
            items.extend(line.strip().split(","))

duplicates = []

for item in items:
    if items.count(item) > 1 and item not in duplicates:
        duplicates.extend(item)

if duplicates:
    print(f"Duplicates: {duplicates}")
else:
    print("No Duplicates")