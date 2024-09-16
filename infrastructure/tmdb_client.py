import requests
from app.config import Config

class TMDbClient:
    PLATFORM_URL = "https://api.themoviedb.org/3/movie/"
    GENERAL_URL = "https://api.themoviedb.org/3/search/movie?query="

    def fetch_streaming_platforms(self, movie_name: int):
        movie_name = movie_name.replace(" ", "+")
        url = f"{self.GENERAL_URL}{movie_name}&api_key={Config.TMDB_API_KEY}"

        response = requests.get(url)
        json_data = response.json()

        movie_id = json_data['results'][0]['id']
        url = f"{self.PLATFORM_URL}{movie_id}/watch/providers?api_key={Config.TMDB_API_KEY}"

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"TMDb API Error: {response.status_code}")
        return response.json()['results']['CO']
