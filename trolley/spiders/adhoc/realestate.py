from __future__ import unicode_literals

import codecs
import urlparse
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup


link = "http://www.realestate.com.au/find-agent/nsw/in-new+south+wales/list-"
pages = xrange(1, 151)


def print_stuff(file, link):
    print link
    r = requests.get(link)
    soup = BeautifulSoup(r.text)

    for i, div in enumerate(soup.find_all("div", {"class": "listingInfo"})):
        cells = []
        try:
            cells.append(div.find("li", {"class" : "fn name"}).h2.a["title"])
        except Exception:
            cells.append(div.find("li", {"class": "fn name"}).h2.a.get_text())
        cells.append(div.find("li", {"class" : "adr"}).get_text())
        cells.append(div.find("li", {"class" : "tel phone"}).a["data-value"])
        try:
            cells.append(div.find("li", {"class" : "url web last"}).a["href"])
        except Exception:
            cells.append("")

        line = "\t".join(cells)
        file.write(line)
        file.write(u"\n")


def get_emails(soup):
    a_tags = soup.find_all("a")
    return ",".join([a["href"] for a in a_tags if "mailto" in a.get("href", "")])


def find_emails(website):
    try:
        r = requests.get(website, timeout=5)
    except Exception:
        return
    soup = BeautifulSoup(r.text, "lxml")
    if "mailto" in r.text:
        return get_emails(soup)
    else:
        a_tags = soup.find_all("a")
        for a in a_tags:
            if "contact" in a.get_text().lower():
                href = a.get("href", "")
                if "http" in href or "www" in href:
                    try:
                        return get_emails(BeautifulSoup(requests.get(href, timeout=5).text, "lxml"))
                    except Exception:
                        continue
                else: #assume relative link
                    parse = urlparse.urlparse(website)
                    try:
                        return get_emails(BeautifulSoup(requests.get(parse.scheme + "://" + parse.hostname + "/" + href, timeout=5).text, "lxml"))
                    except Exception:
                        continue


lines = [line.strip() for line in (open("websites", "rU").readlines())]

pool = Pool(processes=10)
it = pool.imap(find_emails, lines)
results = []
for _ in xrange(len(lines)):
    try:
        print it.next(timeout=10)
    except:
        print "timeout"


def scrape():
    with codecs.open('results.txt', encoding='utf-8', mode="w") as file:
        for p in pages:
            print_stuff(file, link + str(p))
