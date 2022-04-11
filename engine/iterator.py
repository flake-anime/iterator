import requests
from bs4 import BeautifulSoup

class Iterator:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_anime_list(self, page_no):
        page = requests.get(self.base_url + "/anime-list?page=" + str(page_no))
        soup = BeautifulSoup(page.content, 'html.parser')
        anime_components = soup.select(".listing li a", href=True)

        anime_list = []
        for component in anime_components:
            anime_name = component.get_text()
            anime_url = self.base_url + component['href']

            anime = {
                "name": anime_name,
                "url": anime_url
            }

            anime_list.append(anime)

        return anime_list

    def get_a_to_z_list(self, log = False):
        page_no = 1

        a_to_z_list = []
        prev_a_to_z_list = 0

        while True:
            if log:
                print("[*] Getting page " + str(page_no))

            anime_list = self.get_anime_list(page_no)

            for anime in anime_list:
                if not anime in a_to_z_list:
                    a_to_z_list.append(anime)

            if len(a_to_z_list) == prev_a_to_z_list:
                break

            prev_a_to_z_list = len(a_to_z_list)
            page_no += 1
        
        return a_to_z_list