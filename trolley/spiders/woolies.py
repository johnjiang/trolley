from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider
from trolley.items import ShopItem


class WooliesSpider(BaseSpider):
    name = "woolies"

    allowed_domains = ["woolworthsonline.com.au"]
    start_urls = [
        "http://www2.woolworthsonline.com.au",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for department in soup.select("span.navigation-label a"):
            yield Request("%s%s" % (response.url, department["href"]), callback=self.parse_department)

    def parse_department(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        page_links = soup.select(".page-number")  # situation when there's only 1 page of items
        if page_links:
            # we start on the second page because we're already on the first page
            for page_num in xrange(2, int(page_links[-1].text) + 1):
                yield Request("%s&page=%s" % (response.url, page_num), callback=self.parse_page)
        yield self.parse_page(response)

    def parse_page(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        products = soup.select('div.product-stamp-middle')
        for product in products:
            item = ShopItem()
            item['name'] = product.select('div.details-container span.description')[0].text.strip()
            item['price'] = product.select('div.price-container span.price')[0].text.strip()
            item['extra_info'] = product.select('div.price-container div.cup-price')[0].text.strip()
            yield item
