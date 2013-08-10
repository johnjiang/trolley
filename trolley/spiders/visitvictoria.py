from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider

from trolley.helpers import utils
from trolley.items import AccommodationItem


class VisitVictoria(BaseSpider):
    name = "visitvictoria"

    URL = "http://www.visitvictoria.com"
    SEARCH = "http://www.visitvictoria.com/Accommodation/Search.aspx"

    allowed_domains = ["www.visitvictoria.com"]
    start_urls = [
        # bed and breakfasts in victoria, page 1, 50 per page
        "http://www.visitvictoria.com/Accommodation/Search.aspx?region=any&rating=0&cl_2_BF7340E6-D0DC-40C1-8F2B-97451B2813C5=3&facet=%7b823C3295-61EA-462F-9506-AA2F2EA66EBF%7d&page=1&ps=50",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        for item in soup.select(".item"):
            yield Request("%s%s" % (VisitVictoria.URL, utils.select_first_attribute(item, 'h2 a', 'href')), callback=self.parse_item)

        next_page = utils.select_first_attribute(soup, '.next a', 'href')
        if next_page:
            yield Request("%s%s" % (VisitVictoria.SEARCH, next_page), callback=self.parse)

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item = AccommodationItem()

        item["name"] = utils.select_first_text(soup, ".panel.product h1")
        item["email"] = utils.select_first_attribute(soup, ".icon-link-email", "href")
        yield item
