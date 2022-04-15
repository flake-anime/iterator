from engine.iterator import Iterator

iterator = Iterator()

anime_link = "https://ww2.gogoanimes.org/category/death-note-dub"
result = iterator.get_episodes(anime_link)

print(result)