from __future__ import unicode_literals

import codecs

import requests
from bs4 import BeautifulSoup


link = "http://members.reinsw.com.au/Custom/Find_Agent.aspx?Suburb="


def print_stuff(file, link, postcode):
    print link + postcode
    r = requests.get(link + postcode)
    soup = BeautifulSoup(r.text, "lxml")

    table = soup.find("table", {"class": "Grid"})
    if not table:
        return

    for i, tr in enumerate(table.find_all("tr")):
        cells = [postcode]

        for td in tr.find_all("td"):
            cells.append(td.get_text().strip())

            if "Firms per page" in td.get_text():
                return

        line = "\t".join(cells)
        file.write(line)
        file.write(u"\n")


def scrape():
    with codecs.open('results.txt', encoding='utf-8', mode="w") as file:
        for p in open("postcodes.txt").readlines():
            print_stuff(file, link, p.strip())

scrape()
