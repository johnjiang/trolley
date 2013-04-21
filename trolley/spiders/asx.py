from __future__ import unicode_literals
from bisect import bisect_right
import string

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider
from trolley.items import CompanyItem


CATEGORIES = [0, 0.005, 0.01, 0.025, 0.05, 0.10, 0.25, 1]


def urls():
    base_url = "http://www.asx.com.au/asx/research/listedCompanies.do?coName={}"
    yield base_url.format("0")
    for c in string.uppercase:
        yield base_url.format(c)


def find_category(categories, price):
    index = bisect_right(categories, price) - 1
    return categories[index]


class AsxSpider(BaseSpider):
    name = "asx"

    allowed_domains = ["asx.com.au"]
    start_urls = list(urls())

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for a_tag in soup.select("table.contenttable tr td a"):
            yield Request("http://www.asx.com.au/asx/research/{}".format(a_tag["href"]), callback=self.parse_company)

    def parse_company(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = CompanyItem()
        try:
            datatable = soup.select('table.datatable')[0]
            item['name'] = datatable.select('tr th.row')[0].text.strip()
            item['price'] = float(datatable.select('tr td.last')[0].text.strip())
        except Exception:
            print "No prices found for {}".format(response.url)
            item['name'] = response.url[-3:]
            item['price'] = 0

        item["category"] = find_category(CATEGORIES, item['price'])
        yield item
