from __future__ import unicode_literals

import codecs
import urllib2

from bs4 import BeautifulSoup

 
links = """http://functioncentre.com.au/venuesBody.asp?page=1&orderby=
http://functioncentre.com.au/venuesBody.asp?page=2&orderby=
http://functioncentre.com.au/venuesBody.asp?page=3&orderby=
http://functioncentre.com.au/venuesBody.asp?page=4&orderby=
http://functioncentre.com.au/venuesBody.asp?page=5&orderby=
http://functioncentre.com.au/venuesBody.asp?page=6&orderby=""".split("\n")

 
def print_stuff(link):
    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page)

    table = soup.find("table", width="799", border="1")
 
    for n, tr in enumerate(table.find_all("tr")):
        print n
        cells = []
        for i, td in enumerate(tr.find_all("td")):
            if i == 3 and td.a:
                href = td.a.get("href").split("'")[1]
                link = "http://functioncentre.com.au/%s" % href
                popup = BeautifulSoup(urllib2.urlopen(link))
                for td in popup.find_all("td"):
                    if "@" in td.get_text():
                        cells.append(td.get_text().strip())
                        break
            elif i == 4 and td.a:
                cells.append(td.a.get("href"))
            else:
                cells.append(td.get_text())
        file.write(u"\t".join(cells))
        file.write(u"\n")

if __name__ == "__main__":
    with codecs.open('results.txt', encoding='utf-8', mode="w") as file:
        for link in links:
            print_stuff(link)
