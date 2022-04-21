from engine.iterator import get_complete_anime_info

anime_link = "https://ww2.gogoanimes.org/category/009-1"
anime_data = get_complete_anime_info(anime_link)

print(anime_data)