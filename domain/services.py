import requests

class MovieService:
    def __init__(self):
        pass

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


class TMDbService:
    BASE_URL = 'https://api.themoviedb.org/3';
    API_KEY = 'bbf9e364cea80ea7037b2df19efcad88';

    def get_youtube_video(self, media_type, media_id):
        url = f"{self.BASE_URL}/{media_type}/{media_id}/videos"
        params = {
            'api_key': self.API_KEY,
            'language': 'en-US'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_trending(self, media_type, page=1, language=None):
        url = f"{self.BASE_URL}/trending/{media_type}/week"
        params = {
            'api_key': self.API_KEY,
            'page': page,
            'language': language or self.DEFAULT_LANGUAGE
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_recommended(self, media_type, media_id, page=1):
        url = f"{self.BASE_URL}/{media_type}/{media_id}/recommendations"
        params = {
            'api_key': self.API_KEY,
            'page': page,
            'language': 'en-US'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_external_id(self, media_type, media_id):
        url = f"{self.BASE_URL}/{media_type}/{media_id}/external_ids"
        params = {
            'api_key': self.API_KEY
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_movie(self, movie_id):
        url = f"{self.BASE_URL}/movie/{movie_id}"
        params = {
            'api_key': self.API_KEY,
            'language': 'en-US'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_now_playing(self, media_type, page=1):
        url = f"{self.BASE_URL}/{media_type}/now_playing"
        params = {
            'api_key': self.API_KEY,
            'language': 'en-US',
            'page': page
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_content_by_genre(self, genre_id, page=1):
        url = f"{self.BASE_URL}/discover/movie"
        params = {
            'api_key': self.API_KEY,
            'with_genres': genre_id,
            'language': 'en-US',
            'page': page
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_content_by_tipo(self, tipo):
        page = 1
        if tipo.lower() == 'pelicula':
            url = f"{self.BASE_URL}/discover/movie"
        else:
            url = f"{self.BASE_URL}/discover/tv"

        params = {
            'api_key': self.API_KEY,
            'page': page,
            'language': 'en-US'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
