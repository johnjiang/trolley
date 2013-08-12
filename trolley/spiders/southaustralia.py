from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider

from trolley.helpers import utils
from trolley.items import AccommodationItem


class SouthAustralia(BaseSpider):
    name = "southaustralia"

    URL = "http://www.southaustralia.com"

    allowed_domains = ["www.southaustralia.com"]
    start_urls = [
        # bed and breakfasts in SA, page 1
        "http://www.southaustralia.com/search/booking-search.aspx?category=Accommodation&region=All&startDate=2013-08-13&endDate=2013-08-14&type=BEDBREAKFA&adults=1&kids=0&order=BookableFirst&group=SearchAccommodation&searchCity=1&run=1",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        for item in soup.select(".searchResultHolder"):
            yield Request("%s%s" % (self.URL, utils.select_first_attribute(item, '.searchResultHeading a', 'href')), callback=self.parse_item)

        next_page = utils.select_first_attribute(soup, "#SearchResults_lvwPageLinks_lnkNext", 'href')
        if next_page:
            yield Request("%s%s" % (self.URL, next_page), callback=self.parse)

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        item = AccommodationItem()

        item["name"] = utils.select_first_text(soup, ".pagetitle")
        item["email"] = utils.select_first_attribute(soup, "#PageContentUserControl_lnkContactEmail", "href")
        yield item
