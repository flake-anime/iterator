from engine.iterator import Iterator
from database import Database
import json

iterator = Iterator()
anime_data = iterator.get_a_to_z_list(1, 2, log=True)

database = Database("mongodb+srv://animeParadise:Paradise%40anime%3A%2F%2F@anime-paradise.ucpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

for counter, anime in enumerate(anime_data):
    data = iterator.get_extra_info(anime["url"])
    database.insert_data(data)
    print(f"[*] {counter}/{len(anime_data)}")
