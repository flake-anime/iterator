from engine.iterator import Iterator

base_url = "https://ww2.gogoanimes.org"
iterator = Iterator(base_url)

anime_link = "https://ww2.gogoanimes.org/category/death-note-dub" 
result = iterator.get_extra_info(anime_link)

print(result)