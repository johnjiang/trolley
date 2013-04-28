from __future__ import unicode_literals
import csv
from itertools import groupby, izip_longest
import json
from operator import attrgetter
import os
from reports.asx.models import Company


def report(filename):
    Company.CATEGORIES = [0, 0.01, 0.03, 0.16, 0.29, 0.87]

    raw_json = json.load(open(filename, "rU"))
    companies = sorted(map(Company, raw_json), key=attrgetter("letter"))

    rows = []
    for k, g in groupby(companies, key=attrgetter("letter")):
        g = list(g)
        g = sorted(g, key=attrgetter("category"))
        rows.append([k])
        groups = []
        for k2, g2 in groupby(g, key=attrgetter("category")):
            groups.append([k2] + sorted(item.code for item in g2))
        results = map(list, izip_longest(*groups, fillvalue=""))  # transpose lists
        rows += results
        rows.append([])

    with open("formated.csv", "wb") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)


if __name__ == "__main__":
    report(os.path.join("..", "..", "o.txt"))
