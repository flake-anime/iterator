import os
from dotenv import load_dotenv
from database import Database
from engine.iterator import get_complete_anime_info
from engine.iterator import get_a_to_z_list
from database import Database
from engine.wrappers.free_proxy_wrapper import FreeProxyListWrapper
load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
START_PAGE = int(os.getenv("START_PAGE"))
END_PAGE = int(os.getenv("END_PAGE"))

database = Database(CONNECTION_STRING)
proxy = FreeProxyListWrapper()

anime_data = get_a_to_z_list(START_PAGE, END_PAGE, log=True)

for anime in anime_data:
    proxy_ip = proxy.get_random_proxy()
    proxies = { "http": proxy_ip }

    anime_name = anime['name']
    anime_link = anime['url']
    
    print("[*] Getting anime info for " + anime_name + " using proxy " + proxy_ip)
    anime_data = get_complete_anime_info(anime_link, proxies)

    database.insert_data(anime_data)
