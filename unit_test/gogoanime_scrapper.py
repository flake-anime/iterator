import unittest
import tracemalloc
import warnings
from engine.scrappers.gogoanime_scrapper import GogoAnimeScrapper

tracemalloc.start()

class TestGogoAnimeScrapper(unittest.TestCase):

    maxDiff = None

    @classmethod
    def setUpClass(self):
        self.anime_link = "https://ww2.gogoanimes.org/category/death-note-dub"
        self.episode_link = "https://ww2.gogoanimes.org/watch/death-note-dub-episode-1"
        self.player_link = "http://goload.pro/streaming.php?id=OTA3OTk=&title=Death+Note+%28Dub%29&typesub=SUB&sub=&cover=Y292ZXIvZGVhdGgtbm90ZS1kdWIucG5n"

        self.scrapper = GogoAnimeScrapper()

        # Ignoring resourse warnings
        warnings.simplefilter("ignore", ResourceWarning)
    
    @classmethod
    def tearDownClass(self):
        del self.scrapper

    def test_get_anime_list(self):
        result = self.scrapper.get_anime_list(1)
        self.assertGreater(len(result), 0)
    
    def test_get_a_to_z_list(self):
        result = self.scrapper.get_a_to_z_list(1, 2)
        self.assertGreater(len(result), 0)

    def test_get_episodes(self):
        result = self.scrapper.get_episodes(self.anime_link)
        self.assertGreater(len(result), 0)
    
    def test_get_anime_info(self):        
        result = self.scrapper.get_anime_info(self.anime_link)
        self.assertGreater(len(result.keys()), 0)
    
    def test_get_player_link(self):
        result = self.scrapper.get_player_link(self.episode_link)
        expected_result = "http://goload.pro/streaming.php?id=OTA3OTk=&title=Death+Note+%28Dub%29&typesub=SUB&sub=&cover=Y292ZXIvZGVhdGgtbm90ZS1kdWIucG5n"
        self.assertEqual(result, expected_result)

    def test_get_download_link(self):
        result = self.scrapper.get_download_link(self.player_link)
        expected_result = "http://goload.pro/download?id=OTA3OTk%3D&title=Death+Note+%28Dub%29&typesub=SUB&cover=Y292ZXIvZGVhdGgtbm90ZS1kdWIucG5n"
        self.assertEqual(result, expected_result)