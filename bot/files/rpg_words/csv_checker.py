import os,csv

os.chdir(os.path.dirname(__file__))
file = "adjectives.csv"

with open(file,encoding="utf8") as file:
        items = []
        for line in file.readlines():
            items.extend(line.strip().split(","))

for item in items:
    if items.count(item) > 1:
        print(item)