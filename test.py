from engine.iterator import Iterator

iterator = Iterator()

anime_link = "https://ww2.gogoanimes.org/category/009-1"
player_link = iterator.get_player_link(episode_link)

print(player_link)