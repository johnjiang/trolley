from __future__ import unicode_literals
from bisect import bisect_right
import string

from bs4 import BeautifulSoup
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
from trolley.items import CompanyItem


CATEGORIES = [0, 0.002, 0.004, 0.008, 0.01, 0.04, 0.15, 0.69, 0.89]


def urls():
    base_url = "http://www.asx.com.au/asx/research/listedCompanies.do?coName={}"
    yield base_url.format("0-9")
    for c in string.uppercase:
        yield base_url.format(c)


def find_category(categories, price):
    index = bisect_right(categories, price) - 1

    # sanity checks
    assert categories[index] <= price
    if len(categories) != index + 1:
        assert price < categories[index + 1]
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
        asx_code = response.url[-3:]
        item['name'] = soup.select("div#company-information h1")[0].text
        item['code'] = asx_code

        datatables = soup.select('table.datatable')
        if not datatables:
            log.msg("No datatable for: {}".format(asx_code), level=log.ERROR)
            item['price'] = 0
        else:
            try:
                datatable = datatables[0]
                assert datatable.select('tr th.row')[0].text.strip() == asx_code  # sanity check
                price = datatable.select('tr td.last')[0].text.strip()
                item['price'] = float(price or 0)
            except ValueError:
                log.msg("Cannot interpret price for: {}".format(asx_code), level=log.ERROR)
                item['price'] = 0

        item["category"] = find_category(CATEGORIES, item['price'])
        yield item
