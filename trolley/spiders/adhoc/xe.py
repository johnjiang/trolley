from __future__ import unicode_literals

from datetime import datetime
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
import arrow

start = datetime(2007, 1, 1)
end = datetime(2013, 1, 1)

URL = "http://www.xe.com/currencytables/?from=USD&date="
driver = webdriver.PhantomJS()

for r in arrow.Arrow.range('month', start, end):
    url = URL + r.format('YYYY-MM-DD')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.select('#historicalRateTbl tbody')[0]

    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])

    with open('{}.csv'.format(r.format('YYYYMM')), 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
