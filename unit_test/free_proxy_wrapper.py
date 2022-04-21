import unittest
import tracemalloc
from engine.wrappers.free_proxy_wrapper import FreeProxyListWrapper

tracemalloc.start()

class TestIterator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.proxy = FreeProxyListWrapper()

    @classmethod
    def tearDownClass(self):
        del self.proxy
    
    def test_get_proxy_list(self):
        proxy_list = self.proxy.get_proxy_list()
        self.assertIsNotNone(proxy_list)
        self.assertIsInstance(proxy_list, list)
        self.assertGreater(len(proxy_list), 0)
    
    def test_get_random_proxy(self):
        proxy_ip = self.proxy.get_random_proxy()
        self.assertIsNotNone(proxy_ip)
        self.assertIsInstance(proxy_ip, str)
        self.assertGreater(len(proxy_ip), 0)