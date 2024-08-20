import requests
from app.config import Config

class TMDbClient:
    BASE_URL = "https://api.themoviedb.org/3/movie/"

    def fetch_streaming_platforms(self, movie_id: int):
        url = f"{self.BASE_URL}{movie_id}/watch/providers"
        params = {
            'api_key': Config.TMDB_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"TMDb API Error: {response.status_code}")
        return response.json().get('results', {})
