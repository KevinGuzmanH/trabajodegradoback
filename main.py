import requests
import pandas as pd

BASE_URL = "http://www.omdbapi.com/"

params = {
    'apikey': '8bfd7b9c',
    't': 'jack+Reacher'
}
response = requests.get(BASE_URL, params=params)
if response.status_code != 200:
    raise Exception(f"OMDb API Error: {response.status_code}")

movie_data = response.json()

movie_df = pd.DataFrame([movie_data])
print('Dataframe Creado')


