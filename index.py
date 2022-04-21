import os
from dotenv import load_dotenv
from database import Database
from engine.iterator import Iterator
load_dotenv()

connection_string = os.getenv("MONGO_CONNECTION_STRING")
database = Database(connection_string)
iterator = Iterator()

start_page = int(os.getenv("START_PAGE"))
end_page = int(os.getenv("END_PAGE"))

anime_list = iterator.get_a_to_z_list(start_page, end_page)

for anime in anime_list:
    anime_name = anime["name"]
    anime_link = anime["url"]
    
    print("[*] Getting info on " + anime_name)
    print("[*] Anime Link: " + anime_link)
    
    extra_info = iterator.get_extra_info(anime_link)
    print(extra_info)