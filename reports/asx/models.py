from __future__ import unicode_literals
from bisect import bisect_right
import string


def find_category(categories, price):
    index = bisect_right(categories, price) - 1

    # sanity checks
    assert categories[index] <= price
    if len(categories) != index + 1:
        assert price < categories[index + 1]
        return "{} - {}".format(categories[index], categories[index+1])
    return "{}+".format(categories[index])


class Company(object):
    CATEGORIES = None

    def __init__(self, json_dict):
        self.json_dict = json_dict

    def __getattr__(self, item):
        return self.json_dict[item]

    @property
    def category(self):
        return find_category(self.CATEGORIES, self.price)

    @property
    def letter(self):
        if self.name[0].lower() in string.ascii_lowercase:
            return self.name[0]
        else:
            return "0-9"

    @property
    def spread1(self):
        return self.open - self.low

    @property
    def spread2(self):
        return self.high - self.open
