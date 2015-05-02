__author__ = 'edduarte'

import csv

doc = open("triples-data.csv", "r")
reader = csv.reader(doc)

for row in reader:
    print(row[0]+" -- "+row[1]+" -- "+row[2])