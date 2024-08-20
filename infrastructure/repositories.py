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

    def get_streaming_platforms(self, imdb_id: str):
        # Aquí debes mapear el imdb_id al movie_id de TMDb
        # Este paso depende de tu lógica para convertir entre IDs
        movie_id = self._map_imdb_to_tmdb(imdb_id)
        return self.client.fetch_streaming_platforms(movie_id)

    def _map_imdb_to_tmdb(self, imdb_id: str):
        # Implementa la lógica para mapear imdb_id a tmdb_id
        # Esto podría involucrar otra consulta a la API de TMDb
        return 75780  # Ejemplo estático
