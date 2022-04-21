import jikanpy
import requests
import validators
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from jikanpy import Jikan
from urllib.parse import urlparse, urlunparse
from urllib.parse import parse_qs
from engine.wrappers.free_proxy_wrapper import FreeProxyListWrapper

def connection_fail_retry(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            return wrapper(*args, **kwargs)
    return wrapper

def api_exception_retry(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except jikanpy.exceptions.APIException:
            print("[-] APIException, retrying...")
            return wrapper(*args, **kwargs)
    return wrapper

class GogoAnimeScrapper:
    def __init__(self):
        self.gogo_base_url = "https://ww2.gogoanimes.org"
        self.vidstream_base_url = "https://gogoplay4.com"
        self.jikan = Jikan()
        self.proxy = FreeProxyListWrapper()
    
    @connection_fail_retry
    def get_anime_list(self, page_no, proxies = None):
        page = requests.get(self.gogo_base_url + "/anime-list?page=" + str(page_no), proxies=proxies)
        soup = BeautifulSoup(page.content, 'html.parser')
        anime_components = soup.select(".listing li a", href=True)

        anime_list = []
        for component in anime_components:
            anime_name = component.get_text()
            anime_url = self.gogo_base_url + component['href']

            anime = {
                "name": anime_name,
                "url": anime_url
            }

            anime_list.append(anime)

        return anime_list

    def get_a_to_z_list(self, start_page, end_page, log = False, proxy = False):
        page_no = start_page

        a_to_z_list = []
        prev_a_to_z_list = 0

        proxies = None

        while True:
            if page_no == end_page:
                break

            if proxy:
                proxies = {
                    "http": self.proxy.get_random_proxy()
                }

            if log:
                print("[{}/{}] Getting anime list page using proxy {} ...".format(page_no, end_page, proxies["http"] if proxies else "None"))

            anime_list = self.get_anime_list(page_no, proxies = proxies)

            for anime in anime_list:
                if not anime in a_to_z_list:
                    a_to_z_list.append(anime)

            if len(a_to_z_list) == prev_a_to_z_list:
                break

            prev_a_to_z_list = len(a_to_z_list)
            page_no += 1
        
        return a_to_z_list

    @connection_fail_retry
    def get_episodes(self, anime_link, proxies = None):
        api_url = self.gogo_base_url + "/ajaxajax/load-list-episode"
        
        params = {
            "alias": anime_link.replace(self.gogo_base_url, ""),
            "ep_start": "0",
            "ep_end": "",
            "id": "",
            "default_ep": "",
        }
        params = urlencode(params)

        response = requests.get(api_url, params=params, proxies=proxies)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        episodes = []

        episode_components = soup.select("li", href=True)
        for component in episode_components:
            episode_link = self.gogo_base_url + component.find("a")['href'].strip()
            episode_name = component.find(class_="name").get_text()
            episode_number = episode_name.replace("EP ", "")

            episode = {
                "episode_number": episode_number,
                "episode_link": episode_link,
            }

            episodes.append(episode)
        
        return episodes
    
    @connection_fail_retry
    def get_anime_info(self, anime_link, proxies = None):
        page = requests.get(anime_link, proxies=proxies)
        soup = BeautifulSoup(page.content, 'html.parser')

        anime_name = soup.select_one(".anime_info_body h1").get_text()
        gogo_id = anime_link.split("/")[-1]
        cover = soup.select_one(".anime_info_body img")['src']
        type = soup.select_one(".anime_info_body .type a").get_text()
        plot_summary = soup.select(".anime_info_body .type")[1].get_text().replace("Plot Summary: ", "")
        genres = [genre.get_text() for genre in soup.select(".anime_info_body .type")[2].select("a")]
        release = soup.select(".anime_info_body .type")[3].get_text().replace("Released: ", "")
        status = soup.select(".anime_info_body .type")[4].get_text().replace("Status: ", "").strip()
        other_name = [ name.strip() for name in soup.select(".anime_info_body .type")[5].get_text().replace("Other name: ", "").replace("\n", "").split(";") ]

        anime_name_filtered = anime_name.replace("(Dub)", "").replace("(Sub)", "").strip()
        best_match_mal_anime_info = self._get_best_match_mal_anime_info(anime_name_filtered, proxies)
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
    
    @connection_fail_retry
    def _get_best_match_mal_anime_info(self, anime_name, proxies = None):
        # Searching the anime and expanding on the top result
        mal_id = self._get_best_match_mal_id(anime_name, proxies)
        mal_anime_info = self._get_mal_info(mal_id, proxies)
        return mal_anime_info
    
    @connection_fail_retry
    def _get_best_match_mal_id(self, anime_name, proxies = None):
        # Getting best matched mal id from the anime name
        base_url = "https://myanimelist.net/search/all"
        params = {
            "q": anime_name,
            "cat": "all",
        }

        page = requests.get(base_url, params=params, proxies=proxies)
        soup = BeautifulSoup(page.content, 'html.parser')

        top_result_mal_link = soup.select_one(".picSurround a", href=True)
        if top_result_mal_link is None:
            return None

        top_result_mal_link = top_result_mal_link['href']
        mal_id = top_result_mal_link.split("/")[-2]

        return mal_id

    @connection_fail_retry
    def _get_mal_info(self, mal_id, proxies = None):
        # Getting the anime info from the mal id
        mal_url = "https://myanimelist.net/anime/" + str(mal_id)

        page = requests.get(mal_url, proxies=proxies)
        soup = BeautifulSoup(page.content, 'html.parser')

        trailer = soup.select_one(".iframe")
        if trailer is not None:
            trailer = trailer["href"]

        score = soup.select_one(".score-label")
        if score is not None:
            score = score.get_text()

        mal_anime = {
            "trailer_url": trailer,
            "score": score,
            "url": mal_url,
        }

        return mal_anime
    
    @connection_fail_retry
    def get_player_link(self, episode_link, proxies = None):
        gogo_episode_id = episode_link.split("/")[-1]
        vidstream_url = self.vidstream_base_url + "/videos/" + gogo_episode_id

        page = requests.get(vidstream_url, proxies=proxies)
        soup = BeautifulSoup(page.content, 'html.parser')

        player_link = soup.select_one(".play-video iframe")

        if player_link is not None:
            player_link = player_link['src']
            player_link = "http:" + player_link if not validators.url(player_link) else player_link

        return player_link
    
    @connection_fail_retry
    def get_download_link(self, player_link):
        parsed_player_link = urlparse(player_link)

        base_url = urlparse(player_link)
        base_url = base_url.scheme + "://" + base_url.netloc

        params = {
            "id": parse_qs(parsed_player_link.query)['id'][0],
            "title": parse_qs(parsed_player_link.query)['title'][0],
            "typesub": parse_qs(parsed_player_link.query)['typesub'][0],
            "cover": parse_qs(parsed_player_link.query)['cover'][0],
        }

        download_link = urlparse(base_url + "/download")
        encoded_params = urlencode(params)
        download_link = download_link._replace(query=encoded_params)
        download_link = urlunparse(download_link)

        return download_link
        