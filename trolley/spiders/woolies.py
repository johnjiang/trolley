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
        page_links = soup.select(".page-number") # situation when there's only 1 page of items
        if page_links:
            for page_num in xrange(1,int(page_links[-1].text) + 1):
                yield Request("%s&page=%s" % (response.url, page_num), callback=self.parse_page)
        else:
            yield Request("%s" % response.url, callback=self.parse_page)

    def parse_page(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        sites = soup.select('div.product-stamp-middle')
        for site in sites:
            item = ShopItem()
            item['name'] = site.select('div.details-container span.description')[0].text.strip()
            item['price'] = site.select('div.price-container span.price')[0].text.strip()
            item['extra_info'] = site.select('div.price-container div.cup-price')[0].text.strip()
            yield item
