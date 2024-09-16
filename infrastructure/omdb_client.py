import requests
from app.config import Config
import pandas as pd

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

        movie_data = response.json()

        movie_df = pd.DataFrame([movie_data])
        print('Dataframe Creado')

        return movie_data
