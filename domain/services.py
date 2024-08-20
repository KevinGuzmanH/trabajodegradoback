from infrastructure.repositories import OMDbRepository, TMDbRepository

class MovieService:
    def __init__(self):
        self.omdb_repo = OMDbRepository()
        self.tmdb_repo = TMDbRepository()

    def get_movie_info(self, title: str):
        movie_data = self.omdb_repo.get_movie_info(title)
        platforms = self.tmdb_repo.get_streaming_platforms(movie_data['imdbID'])
        movie_data['streaming_platforms'] = platforms
        return movie_data
