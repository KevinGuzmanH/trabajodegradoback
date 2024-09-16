from unittest.mock import patch
from flask import jsonify

def test_get_movie_info(client):
    movie_data_mock = {
        "Title": "Titanic",
        "Year": "1997",
        "imdbID": "tt0120338",
        "Type": "movie",
        "Response": "True"
    }

    platforms_mock = {
        "link": "https://www.themoviedb.org/movie/597-titanic/watch?locale=CO",
        "flatrate": [
            {
                "display_priority": 0,
                "logo_path": "/97yvRBw1GzX7fXprcF80er19ot.jpg",
                "provider_id": 337,
                "provider_name": "Disney Plus"
            },
            {
                "display_priority": 2,
                "logo_path": "/pbpMk2JmcoNnQwx5JGpXngfoWtp.jpg",
                "provider_id": 8,
                "provider_name": "Netflix"
            }
        ],
    }

    with patch('infrastructure.repositories.OMDbRepository.get_movie_info', return_value=movie_data_mock):
        with patch('infrastructure.repositories.TMDbRepository.get_streaming_platforms', return_value=platforms_mock):
            response = client.get('/movie/Titanic')
            assert response.status_code == 200
            data = response.get_json()
            assert data['Title'] == "Titanic"
            assert 'streaming_platforms' in data
            assert 'flatrate' in data['streaming_platforms']
