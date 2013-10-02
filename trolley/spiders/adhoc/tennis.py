from __future__ import unicode_literals

import codecs
import urllib2

from bs4 import BeautifulSoup


def print_stuff(code, link=None):
    print link
    s = "http://www.tennis.com.au/?type=Coaches&s="
    link = link or s + code

    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page)

    coaches = soup.find_all("li", {"class": "markers one-third vcard"})

    for c in coaches:
        cells = {}
        location = c.find("a", {"class": "gmap_locate_button block"})
        if location:
            cells["location"] = " ".join(location["rel"])
        address = c.find("span", {"class": "addr hidden"})
        if address:
            cells["address"] = address.get_text()
        for i, li in enumerate(c.find_all("li")):
            if i == 0:
                cells["title"] = li.get_text().strip().replace("\n", " ")
            elif i == 1:
                try:
                    cells["phone"] = li.span.get_text().strip(" or ")
                except Exception:
                    pass
                cells["email"] = li.a["title"][6:]

        file.write("\t".join(
            [cells.get("title", ""), cells.get("phone", ""),
             cells.get("email", ""), cells.get("location", ""),
             cells.get("address", "")]))
        file.write("\n")

    # find next page
    next = soup.find("div", {"class": "block float-right"})
    for a in next.find_all("a"):
        if "next" in a.get_text().lower():
            print_stuff(code, "http://www.tennis.com.au/" + a["href"])


with codecs.open('results.txt', encoding='utf-8', mode="w") as file:
    lines = [l.strip() for l in open("postcodes.txt", "rU").readlines()]
    for l in lines:
        print_stuff(l)
        print l
