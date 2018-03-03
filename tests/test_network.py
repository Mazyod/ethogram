import unittest
from ethogram.network import Network


class NetworkTests(unittest.TestCase):
    def test_fetch_all_rigs(self):
        network = Network()
        rigs = network.fetch_rigs("mazyod")

        self.assertEqual(len(rigs), 1)
        self.assertEqual(rigs[0].name, "mastery")
