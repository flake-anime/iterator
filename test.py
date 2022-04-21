from engine.iterator import Iterator

iterator = Iterator()

episode_link = "https://ww2.gogoanimes.org/watch/009-1-dub-episode-1"
player_link = iterator.get_player_link(episode_link)

print(player_link)