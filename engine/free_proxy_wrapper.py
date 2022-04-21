import requests
import random
from bs4 import BeautifulSoup
from urllib3 import proxy_from_url

class FreeProxyListWrapper:
    def get_proxy_list(self):
        page = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(page.content, 'html.parser')
        proxy_list = soup.select_one("textarea").get_text().split("\n")[3:-1]
        return proxy_list
    
    def get_random_proxy(self):
        proxy_list = self.get_proxy_list()
        random_proxy = random.choice(proxy_list)
        return random_proxy