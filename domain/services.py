import requests
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from flask import jsonify

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
            'language': 'es-ES'
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
            'language': 'es-ES'
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
            'language': 'es-ES'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_now_playing(self, media_type, page=1):
        url = f"{self.BASE_URL}/{media_type}/now_playing"
        params = {
            'api_key': self.API_KEY,
            'language': 'es-ES',
            'page': page
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def get_content_by_genre(self, genre_id, page=1):
        url = f"{self.BASE_URL}/discover/movie?api_key={self.API_KEY}&with_genres={genre_id}&language=es-ES&page={page}"
        response = requests.get(url)
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
            'language': 'es-ES'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

class IAService:
    def __init__(self):
        # Configurar la conexión a PostgreSQL
        self.engine = create_engine('postgresql+psycopg2://postgres:grado122@localhost/grado')

    def load_data(self):
        # Consultas SQL para obtener los datos
        self.preferences_query = """
            SELECT user_id, watch_frequence_by_week, netflix_favorite_platform, amazon_prime_favorite_platform, 
                   disney_prime_favorite_platform, hbo_prime_favorite_platform, like_accion_genre, 
                   like_aventura_genre, like_animacion_genre, like_comedia_genre, like_crimen_genre,
                   like_documental_genre, like_drama_genre, like_familiar_genre, like_fantasia_genre, 
                   like_historia_genre, like_horror_genre, like_musica_genre, like_misterio_genre,
                   like_romance_genre, like_ciencia_ficcion_genre, like_guerra_genre
            FROM user_preferences;
        """

        self.interactions_query = """
            SELECT user_id, content_id, content_type ,liked
            FROM user_interactions;
        """

        self.recomendations_query = """
            SELECT user_id,
            Accion,
            Aventura,
            Animacion,
            Comedia,
            Crimen,
            Documental,
            Drama,
            Familiar,
            Fantasia,
            Historia,
            Horror,
            Musica,
            Misterio,
            Romance,
            Ciencia,
            Guerra
            FROM recommendations;
        """

        # Cargar datos
        self.preferences_df = pd.read_sql(self.preferences_query, self.engine)
        self.interactions_df = pd.read_sql(self.interactions_query, self.engine)
        self.recommendations_df = pd.read_sql(self.recomendations_query, self.engine)

        self.preferences_df.replace({True: 1, False: 0}, inplace=True)
        self.interactions_df.replace({True: 1, False: 0}, inplace=True)
        self.interactions_df.replace({'movie': 1, 'serie': 0}, inplace=True)
        self.recommendations_df.replace({True: 1, False: 0}, inplace=True)
        self.recommendations_df.replace({'movie': 1, 'serie': 0}, inplace=True)

    def createdataframe(self):
        import pandas as pd
        import numpy as np

        X = self.X

        # DataFrame para y (los géneros de recomendaciones)
        y = self.y

        # Crear un mapeo entre columnas de preferencias (X) y géneros (y)
        mapping = {
            'like_accion_genre': 'accion',
            'like_aventura_genre': 'aventura',
            'like_animacion_genre': 'animacion',
            'like_comedia_genre': 'comedia',
            'like_crimen_genre': 'crimen',
            'like_documental_genre': 'documental',
            'like_drama_genre': 'drama',
            'like_familiar_genre': 'familiar',
            'like_fantasia_genre': 'fantasia',
            'like_historia_genre': 'historia',
            'like_horror_genre': 'horror',
            'like_musica_genre': 'musica',
            'like_misterio_genre': 'misterio',
            'like_romance_genre': 'romance',
            'like_ciencia_ficcion_genre': 'ciencia',
            'like_guerra_genre': 'guerra'
        }

        # Iterar sobre el mapeo y ajustar los valores en y
        for preference, genre in mapping.items():
            # Si la preferencia en X es 1 (alta), aumentar el valor correspondiente en y
            if X[preference].iloc[0] == 1:
                y[genre].iloc[0] = np.random.randint(50, 100)  # Valores altos para géneros favoritos
            else:
                y[genre].iloc[0] = np.random.randint(0, 50)  # Valores más bajos para géneros menos favoritos

        return y

    def get_recommendations_for_user(self, user_id):

        # Cargar los datos al iniciar la clase
        self.load_data()

        # Unir las preferencias y las interacciones
        self.user_data = pd.merge(self.preferences_df, self.interactions_df, on='user_id', how='left')
        self.user_data = self.user_data[self.user_data['user_id'] == user_id]

        # Llenar los valores NaN con 0 o False
        self.user_data = self.user_data.fillna(0)

        # Pivot the content_id and liked to create separate columns for each
        self.user_data['content_id'] = self.user_data['content_id'].astype(str)
        self.user_data['liked'] = self.user_data['liked'].astype(str)

        # Enumerar los contenidos por usuario
        self.user_data['content_rank'] = self.user_data.groupby('user_id').cumcount() + 1

        # Pivotear los content_id y liked
        self.user_data_pivot = self.user_data.pivot(index='user_id', columns='content_rank',
                                                    values=['content_id', 'liked'])

        # Renombrar las columnas
        self.user_data_pivot.columns = [f'{col[0]}_{col[1]}' for col in self.user_data_pivot.columns]

        # Unir con las preferencias
        self.final_user_data = pd.merge(self.preferences_df, self.user_data_pivot, on='user_id', how='left')

        # Crear X (características) y y (etiquetas)
        self.X = self.final_user_data[self.final_user_data['user_id'] == user_id]
        self.y = self.recommendations_df[self.recommendations_df['user_id'] == user_id]

        # Entrenar un modelo de árbol de decisión
        self.clf = DecisionTreeClassifier()
        self.clf.fit(self.X, self.y)

        fited = self.createdataframe()
        # Usar el modelo para predecir la probabilidad de que le guste cierto contenido
        predicted_content = self.clf.predict(self.X)

        predicted_content = predicted_content.tolist()
        fited = fited.values.tolist()
        # Devolver la respuesta en formato JSON
        return fited

