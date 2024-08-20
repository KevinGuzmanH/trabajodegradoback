import requests
from app.config import Config

class OMDbClient:
    BASE_URL = "http://www.omdbapi.com/"

    def fetch_movie(self, title: str):
        params = {
            'apikey': Config.OMDB_API_KEY,
            't': title
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"OMDb API Error: {response.status_code}")
        return response.json()
