import os
from dotenv import load_dotenv
from database import Database
from engine.iterator import Iterator
from database import Database
from engine.free_proxy_wrapper import FreeProxyListWrapper
load_dotenv()

connection_string = os.getenv("MONGO_CONNECTION_STRING")

database = Database(connection_string)
iterator = Iterator()
proxy = FreeProxyListWrapper()

anime_data = iterator.get_a_to_z_list(1, 2, log=True)

for anime in anime_data:
    proxy_ip = proxy.get_random_proxy()

    proxies = {
        "http": proxy_ip,
    }

    anime_name = anime['name']
    anime_link = anime['url']
    
    print("[*] Getting episodes for " + anime_name + " using proxy " + proxy_ip)

    extra_info = iterator.get_extra_info(anime_link, proxies)
    episode_links = iterator.get_episodes(anime_link, proxies)
    
    episodes = []

    for episode_link in episode_links:
        episode_number = episode_link['episode_number']
        episode_link = episode_link['episode_link']
        player_link = iterator.get_player_link(episode_link, proxies)
        download_link = iterator.get_download_link(player_link)

        episode = {
            "episode_number": episode_number,
            "episode_link": episode_link,
            "player_link": player_link,
            "download_link": download_link,
        }

        episodes.append(episode)

