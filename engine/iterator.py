import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from jikanpy import Jikan

class Iterator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.jikan = Jikan()
    
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

    def get_episodes(self, anime_link):
        api_url = self.base_url + "/ajaxajax/load-list-episode"
        
        params = {
            "alias": anime_link.replace(self.base_url, ""),
            "ep_start": "0",
            "ep_end": "",
            "id": "",
            "default_ep": "",
        }
        params = urlencode(params)

        response = requests.get(api_url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        episodes = []

        episode_components = soup.select("li", href=True)
        for component in episode_components:
            episode_link = self.base_url + component.find("a")['href'].strip()
            episode_name = component.find(class_="name").get_text()
            episode_number = episode_name.replace("EP ", "")

            episode = {
                "ep": episode_number,
                "link": episode_link,
            }

            episodes.append(episode)
        
        return episodes
    
    def get_extra_info(self, anime_link):
        page = requests.get(anime_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        anime_name = soup.select_one(".anime_info_body h1").get_text()
        gogo_id = anime_link.split("/")[-1]
        cover = soup.select_one(".anime_info_body img")['src']
        type = soup.select_one(".anime_info_body .type a").get_text()
        plot_summary = soup.select(".anime_info_body .type")[1].get_text().replace("Plot Summary: ", "")
        genres = [genre.get_text() for genre in soup.select(".anime_info_body .type")[2].select("a")]
        release = soup.select(".anime_info_body .type")[3].get_text().replace("Released: ", "")
        status = soup.select(".anime_info_body .type")[4].get_text().replace("Status: ", "")
        other_name = soup.select(".anime_info_body .type")[5].get_text().replace("Other name: ", "").strip()

        anime_name_filtered = anime_name.replace("(Dub)", "").replace("(Sub)", "").strip()
        best_match_mal_anime_info = self._get_best_match_mal_anime_info(anime_name_filtered)
        trailer = best_match_mal_anime_info['trailer_url']
        score = best_match_mal_anime_info['score']
        mal_url = best_match_mal_anime_info['url']

        anime = {
            "anime_name": anime_name,
            "gogo_id": gogo_id,
            "cover": cover,
            "type": type,
            "plot_summary": plot_summary,
            "genres": genres,
            "release": release,
            "status": status,
            "other_name": other_name,
            "trailer": trailer,
            "score": score,
            "url": mal_url,
        }

        return anime
    
    def _get_best_match_mal_anime_info(self, anime_name):
        # Searching the anime and expanding on the top result
        search_result = self.jikan.search('anime', anime_name, page=1)
        anime = self.jikan.anime(search_result['results'][0]['mal_id'])

        return anime