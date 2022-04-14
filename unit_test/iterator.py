from logging import warning
import unittest
import tracemalloc
import warnings
from engine.iterator import Iterator

tracemalloc.start()

class TestIterator(unittest.TestCase):

    def setUp(self):
        base_url = "https://ww2.gogoanimes.org"

        self.anime_link = "https://ww2.gogoanimes.org/category/death-note-dub"
        self.episode_link = "https://ww2.gogoanimes.org/watch/death-note-dub-episode-1"

        self.iterator = Iterator(base_url)

        # Ignoring resourse warnings
        warnings.simplefilter("ignore", ResourceWarning)
    
    def tearDown(self):
        del self.iterator

    def test_get_anime_list(self):
        result = self.iterator.get_anime_list(1)
        self.assertGreater(len(result), 0)
    
    def test_get_a_to_z_list(self):
        result = self.iterator.get_a_to_z_list()
        self.assertGreater(len(result), 0)

    def test_get_episodes(self):
        result = self.iterator.get_episodes(self.anime_link)
        self.assertGreater(len(result), 0)
    
    def test_get_extra_info(self):        
        result = self.iterator.get_extra_info(self.anime_link)
        expected_result = {
            'anime_name': 'Death Note (Dub)', 
            'gogo_id': 'death-note-dub', 
            'cover': 'https://gogocdn.net/cover/death-note-dub.png', 
            'type': 'TV Series', 
            'plot_summary': 'Yagami Light is a 17-year-old genius from Japan who is tired of his life, school, and the state of the world as he knows it. One day, on the way home from class, Light stumbles upon a dark notebook with "Death Note" written on the front. Intrigued by its appearance, Light reads the first few sentences, only to find out that it states that anyone whose name is written inside will die. Discarding it as a joke, Light continues his daily activities. Soon after though, his human curiosity takes the better of him and prompts Light to try the notebook, discovering the truth behind first sentence. Now, with power in his hands, Yagami Light is on a quest to change the world and become God of the New World. His path to holy status won\'t be easy however, as another genius, known as L, is working against Light\'s beliefs and Light himself. Who will win this power of Gods between humans?', 
            'genres': ['Drama', 'Mystery', 'Police', 'Psychological', 'Shounen', 'Supernatural', 'Thriller'], 
            'release': '2003', 
            'status': 'Completed', 
            'other_name': 'デスノート', 
            'trailer': None, 
            'score': 7.69, 
            'url': 'https://myanimelist.net/anime/2994/Death_Note__Rewrite'
        }

        self.assertEqual(result, expected_result)
    
    def test_get_player_link(self):
        result = self.iterator.get_player_link(self.episode_link)
        expected_result = "https://ww.9anime2.com/embed/OTA3OTk="
        self.assertEqual(result, expected_result)