import unittest
from ethogram.util import Util

class UtilTests(unittest.TestCase):
    def test_min_max_from_seq(self):
        self.assertEqual(Util.min_max_from_seq("4 2 1 8 3"), (1, 8))
        self.assertEqual(Util.min_max_from_seq("2"), (2, 2))
        self.assertEqual(Util.min_max_from_seq(""), (0, 0))

    def test_time_ago(self):
        self.assertEqual(Util.time_ago(1), "1s")
        self.assertEqual(Util.time_ago(66), "1m")
        self.assertEqual(Util.time_ago(60 * 60 * 3), "3h")
        self.assertEqual(Util.time_ago(60 ** 4), "150d")
