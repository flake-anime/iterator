from engine.scrappers.gogoanime_scrapper import GogoAnimeScrapper

scrapper = GogoAnimeScrapper()

def get_a_to_z_list(start_page, end_page, log = False, proxy = False):
    end_page = end_page + 1
    a_to_z_list = scrapper.get_a_to_z_list(start_page, end_page, log, proxy)
    return a_to_z_list

def get_complete_anime_info(anime_link, proxies = None):
    anime_info = scrapper.get_anime_info(anime_link, proxies)
    episode_links = scrapper.get_episodes(anime_link, proxies)
    
    episodes = []

    for episode_link in episode_links:
        episode_number = episode_link['episode_number']
        episode_link = episode_link['episode_link']

        player_link = scrapper.get_player_link(episode_link, proxies)

        download_link = None
        if player_link is not None:
            download_link = scrapper.get_download_link(player_link)

        episode = {
            "episode_number": episode_number,
            "episode_link": episode_link,
            "player_link": player_link,
            "download_link": download_link,
        }

        episodes.append(episode)

    anime_info['episodes'] = episodes

    return anime_info