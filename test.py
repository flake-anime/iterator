from engine.scrappers.gogoanime_scrapper import GogoAnimeScrapper

scrapper = GogoAnimeScrapper()

player_link = "http://goload.pro/streaming.php?id=NDYyNjE=&title=&typesub=SUB&sub=&cover=aW1hZ2VzL2FuaW1lL0QvMzE0MzMuanBn"
download_link = scrapper.get_download_link(player_link)

print(download_link)