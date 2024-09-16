from domain.repositories import MovieRepository
from .omdb_client import OMDbClient
from .tmdb_client import TMDbClient

class OMDbRepository(MovieRepository):
    def __init__(self):
        self.client = OMDbClient()

    def get_movie_info(self, title: str):
        return self.client.fetch_movie(title)

class TMDbRepository:
    def __init__(self):
        self.client = TMDbClient()

    def get_streaming_platforms(self, omdb_title: str):
        return self.client.fetch_streaming_platforms(omdb_title)

