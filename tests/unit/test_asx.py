import unittest
from trolley.spiders.asx import find_category


class TestAsx(unittest.TestCase):
    def test_find_category(self):
        c = [0, 0.005, 0.01, 0.025, 0.05, 0.10, 0.25, 1]
        self.assertEquals(find_category(c, 0), 0)
        self.assertEquals(find_category(c, 0.003), 0)
        self.assertEquals(find_category(c, 0.005), 0.005)
        self.assertEquals(find_category(c, 0.006), 0.005)
        self.assertEquals(find_category(c, 1), 1)
        self.assertEquals(find_category(c, 100), 1)
