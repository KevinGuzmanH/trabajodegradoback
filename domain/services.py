
class MovieService:
    def __init__(self):
        pass  # Aquí no inicializamos directamente las repos

    def get_movie_info(self, title: str):
        from infrastructure.repositories import OMDbRepository, TMDbRepository
        omdb_repo = OMDbRepository()
        tmdb_repo = TMDbRepository()

        movie_data = omdb_repo.get_movie_info(title)
        if 'Title' not in movie_data:
            return {'error': 'Película no encontrada'}, 404

        platforms = tmdb_repo.get_streaming_platforms(movie_data['Title'])
        movie_data['streaming_platforms'] = platforms
        return movie_data, 200
