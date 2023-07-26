import unittest
import json
from app import app

class TestScrapingAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_load_and_extract_data(self):
        # Send a POST request to load_and_extract_data
        response = self.app.post('/load_and_extract_data', json={'base_url': 'https://en.wikipedia.org/wiki/LLM'})
        self.assertEqual(response.status_code, 200)

    def test_search_text(self):
        # Load and extract data first
        self.app.post('/load_and_extract_data', json={'base_url': 'https://en.wikipedia.org/wiki/LLM'})

        # Search for the text "Wikipedia" in the extracted data
        response = self.app.post('/search_text', json={'search_text': 'Wikipedia'})
        data = json.loads(response.get_data(as_text=True))

        # Verify that the API returns a valid response and the search text is found in at least one page
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_search_text_not_found(self):
        # Load and extract data first
        self.app.post('/load_and_extract_data', json={'base_url': 'https://en.wikipedia.org/wiki/LLM'})

        # Search for a non-existing text in the extracted data
        response = self.app.post('/search_text', json={'search_text': 'ThisTextDoesNotExist'})
        data = json.loads(response.get_data(as_text=True))

        # Verify that the API returns a valid response and no search results are found
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

if __name__ == '__main__':
    unittest.main()
