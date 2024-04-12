import requests
from config import settings

def fetch_popular_movies(api_key=settings.API_KEY):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        response.raise_for_status()

def fetch_movie_genres(api_key=settings.API_KEY):
    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['genres']
    else:
        response.raise_for_status()