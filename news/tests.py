from django.test import TestCase

from news.hackerAPI import GetRecentNewsID

class HackerAPITests(TestCase):
    def test_get_top_news_response_not_none_type(self):

        response = GetTopNewsID()
        self.assertIsNotNone(response, "An empty array is expected as response")
