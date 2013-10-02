from __future__ import unicode_literals
import codecs

import requests
from bs4 import BeautifulSoup



link = "http://www.visitnsw.com/accommodation/search?query=&meta_D_phrase_orsand=&meta_k_phrase_orsand=%22Bed%20and%20Breakfasts%22&ge_p=&le_q=&meta_s=&start_rank="
root = "http://www.visitnsw.com"
pages = range(1, 655, 20)


def print_stuff(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)

    for i, dd in enumerate(soup.find_all("dd", {"class": "view-details"})):
        cells = []
        href = dd.a["href"]
        detail = root + href

        b = BeautifulSoup(requests.get(detail).text)
        header = b.find(id="content-main").h1.get_text()

        try:
            email = b.find("dd", {"class": "email"}).a.get_text()
        except Exception:
            email = ""

        cells.append(header)
        cells.append(email)

        line = u"\t".join(cells)
        print line

        file.write(line)
        file.write(u"\n")


with codecs.open('results.txt', encoding='utf-8', mode="w") as file:
    for p in pages:
        print_stuff(link + str(p))
