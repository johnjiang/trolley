from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider
from selenium import webdriver

from trolley.helpers import utils
from trolley.items import AccommodationItem


class WesternAustralia(BaseSpider):
    name = "westernaustralia"

    URL = "http://www.westernaustralia.com"

    allowed_domains = ["www.westernaustralia.com"]
    start_urls = [
        # bed and breakfasts in WA, page 1, 100 per page
        "http://www.westernaustralia.com/au/search/Pages/Accommodation_Search.aspx?&clas=Bed+and+Breakfasts%2c&cat=Accommodation&p=1&rpp=100&sort=Bookable&nadults=1",
    ]

    driver = webdriver.PhantomJS()

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        for item in soup.select(".resultWrapper"):
            yield Request(utils.select_first_attribute(item, '.resultLeft h3 a', 'href'), callback=self.parse_item)

        page_info = soup.select("[id*=pagingInfo_Bottom]")[0]
        is_next = page_info.select("[id*=Results_cmdNext_Bottom]")
        if is_next:
            next_page = page_info.select('span a')[-1]
            yield Request("%s%s" % (self.URL, next_page['href']), callback=self.parse)

    def parse_item(self, response):
        self.driver.get(response.url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        item = AccommodationItem()

        item["name"] = utils.select_first_text(soup, "#product_title")
        item["email"] = utils.select_first_attribute(soup, "#email a", "href")
        yield item
