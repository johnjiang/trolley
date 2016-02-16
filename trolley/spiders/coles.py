from __future__ import unicode_literals

from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.spider import BaseSpider
from selenium import webdriver
from trolley.helpers.utils import select_first_text

from trolley.items import ShopItem


class ColesSpider(BaseSpider):
    name = "coles"

    allowed_domains = ["shop.coles.com.au"]
    start_urls = [
        "http://shop.coles.com.au/online/national/",
    ]

    @property
    def driver(self):
        if not hasattr(self, '_driver'):
            self._driver = webdriver.PhantomJS()
        return self._driver

    def parse(self, response):
        body = response.body.decode('unicode_escape')  # remove unicode crap
        body = body.replace("</html>", "")  # stupid coles has extra closing html tag
        soup = BeautifulSoup(body, 'lxml')
        for aisle in soup.select('#aisleMenu li div ul li a'):
            yield Request(aisle["href"], callback=self.parse_aisle)

    def parse_aisle(self, response):
        self.driver.get(response.url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        for item in self.parse_page(soup):
            yield item

        while soup.select('.next a'):
            self.driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            for item in self.parse_page(soup):
                yield item

    def parse_page(self, soup):
        for item in soup.select('.wrapper.clearfix'):
            name = select_first_text(item, '.item a')
            price = select_first_text(item, '.price')
            yield ShopItem(name=name, price=price)
