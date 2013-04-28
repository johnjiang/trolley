from __future__ import unicode_literals
import string

from bs4 import BeautifulSoup
from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider
from trolley.items import CompanyItem

LAST_ID = 0
CHANGE_ID = 1
BID_ID = 2
OFFER_ID = 3
OPEN_ID = 4
HIGH_ID = 5
LOW_ID = 6
VOL_ID = 7

COLUMN_MAPPER = {
    "price": LAST_ID,
    "change": CHANGE_ID,
    "bid": BID_ID,
    "offer": OFFER_ID,
    "open": OPEN_ID,
    "high": HIGH_ID,
    "low": LOW_ID,
    "vol": VOL_ID
}


def urls():
    base_url = "http://www.asx.com.au/asx/research/listedCompanies.do?coName={}"
    yield base_url.format("0-9")
    for c in string.uppercase:
        yield base_url.format(c)


class AsxSpider(BaseSpider):
    name = "asx"

    allowed_domains = ["asx.com.au"]
    start_urls = list(urls())

    def get_num(self, field):
        field = field.replace("%", "").replace(",", "")
        try:
            return float(field or 0)
        except ValueError:
            return 0

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
            datatable = datatables[0]
            assert datatable.select('tr th.row')[0].text.strip() == asx_code  # sanity check
            for key, column_id in COLUMN_MAPPER.items():
                item[key] = self.get_num(datatable.select('tr td')[column_id].text.strip())
        yield item
