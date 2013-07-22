from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider
from trolley.helpers import utils
from trolley.items import TrueLocalItem


class TrueLocalSpider(BaseSpider):
    name = "truelocal"

    URL = "http://www.truelocal.com.au"

    allowed_domains = ["www.truelocal.com.au"]
    start_urls = [
        "http://www.truelocal.com.au/search/personal-trainers/melbourne-greater-metro%2c-vic",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for item in soup.select("li.search-item a"):
            yield Request("%s%s" % (TrueLocalSpider.URL, item["href"]), callback=self.parse_item)

        next_page = soup.select("div#pagination li")[-1].select("a")
        if next_page:
            yield Request("%s%s" % (TrueLocalSpider.URL, next_page[0]["href"]), callback=self.parse)

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = TrueLocalItem()
        item["url"] = response.url

        item["name"] = utils.select_first_text(soup, "h1[itemprop=name]")

        try:
            address = soup.select("li#business-address")[0]
        except:
            address = None

        item["street"] = utils.select_first_text(address, "strong[itemprop=streetAddress]")
        item["suburb"] = utils.select_first_text(address, "span[itemprop=addressLocality]")
        item["state"] = utils.select_first_text(address, "span[itemprop=addressRegion]")

        item["local_phone"] = utils.select_first_attribute(soup, "a[phonetype=local]", "phonenumber")
        item["mobile_phone"] = utils.select_first_attribute(soup, "a[phonetype=mobile]", "phonenumber")
        item["fax_phone"] = utils.select_first_attribute(soup, "a[phonetype=fax]", "phonenumber")

        item["website"] = utils.select_first_attribute(soup, "li#business-links a.url", "href")
        yield item
