import os
from dotenv import load_dotenv
from database import Database
from engine.iterator import get_complete_anime_info
from engine.iterator import get_a_to_z_list
from database import Database
from engine.wrappers.free_proxy_wrapper import FreeProxyListWrapper
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
START_PAGE = int(os.getenv("START_PAGE"))
END_PAGE = int(os.getenv("END_PAGE"))

database = Database(CONNECTION_STRING)
proxy = FreeProxyListWrapper()

anime_list = get_a_to_z_list(START_PAGE, END_PAGE, log=False)

total_anime = len(anime_list)
progress = 0

def expand_on_anime_from_anime_list_and_upload_to_database(anime, log = False):
    proxy_ip = proxy.get_random_proxy()
    proxies = { "http": proxy_ip }

    anime_name = anime['name']
    anime_link = anime['url']
    
    if log:
        print("[*] Getting anime info for " + anime_name + " using proxy " + proxy_ip)
        
    anime_data = get_complete_anime_info(anime_link, proxies)
    
    return anime_data

if __name__ == "__main__":
    futures = []

    print("[*] Starting the thread pool")

    with ThreadPoolExecutor(max_workers=1000) as executor:
        for anime_data in tqdm(
            executor.map(expand_on_anime_from_anime_list_and_upload_to_database, anime_list), 
            desc="Crawling Data", 
            total=total_anime
        ):
            database.insert_anime(anime_data)
