from engine.iterator import Iterator

base_url = "https://ww2.gogoanimes.org"
iterator = Iterator(base_url)

anime_link = "https://ww2.gogoanimes.org/category/tribe-nine-dub" 
result = iterator.get_episodes(anime_link)

print(result)