from engine.iterator import Iterator

iterator = Iterator()

episode_link = "https://ww2.gogoanimes.org/watch/death-note-dub-episode-1" 
result = iterator.get_player_link(episode_link)

print(result)