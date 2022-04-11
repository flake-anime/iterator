import unittest
from engine.iterator import Iterator

class TestIterator(unittest.TestCase):

    def setUp(self):
        base_url = "https://ww2.gogoanimes.org"
        self.iterator = Iterator(base_url)
    
    def tearDown(self):
        self.iterator = None

    def test_get_anime_list(self):
        result = self.iterator.get_anime_list(1)
        self.assertGreater(len(result), 0)
    
    def test_get_a_to_z_list(self):
        result = self.iterator.get_a_to_z_list()
        self.assertGreater(len(result), 0)