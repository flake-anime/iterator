from engine.iterator import Iterator

iterator = Iterator()

player_link = "http://goload.pro/streaming.php?id=OTA3OTk=&title=Death+Note+%28Dub%29&typesub=SUB&sub=&cover=Y292ZXIvZGVhdGgtbm90ZS1kdWIucG5n" 
result = iterator.get_download_link(player_link)

print(result)