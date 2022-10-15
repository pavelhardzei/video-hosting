from unittest.mock import ANY

from base.schemas.enums import ErrorCodeEnum
from base.utils.consts import DATETIME_FMT
from content.schemas.enums import MediaContentTypeEnum
from fastapi import status
from tests import client
from tests.content.factories import ContentFactory, MovieFactory
from tests.utils import count_queries


def test_movie(movie):
    response = client.get(f'/api/v1/content/movies/{movie.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'content_type': MediaContentTypeEnum.movie,
        'id': movie.id,
        'title': movie.content.title,
        'description': movie.content.description,
        'year': movie.content.year,
        'release_date': movie.content.release_date.strftime(DATETIME_FMT),
        'age_limit': movie.content.age_limit,
        'poster': movie.content.poster,
        'background': movie.content.background,
        'imdb_rating': movie.content.imdb_rating,
        'imdb_vote_count': movie.content.imdb_vote_count,
        'kinopoisk_rating': movie.content.kinopoisk_rating,
        'kinopoisk_vote_count': movie.content.kinopoisk_vote_count,
        'countries': [
            {
                'name': ANY,
                'abbr': ANY,
                'code': ANY,
                'id': ANY
            },
            {
                'name': ANY,
                'abbr': ANY,
                'code': ANY,
                'id': ANY
            }
        ],
        'genres': [
            {
                'name': ANY,
                'id': ANY
            },
            {
                'name': ANY,
                'id': ANY
            }
        ],
        'actors': [
            {
                'name': ANY,
                'id': ANY
            },
            {
                'name': ANY,
                'id': ANY
            }
        ],
        'directors': [
            {
                'name': ANY,
                'id': ANY
            },
            {
                'name': ANY,
                'id': ANY
            }
        ],
        'source': movie.media.source,
        'preview': movie.media.preview,
        'duration': movie.media.duration,
        'created_at': movie.media.created_at.strftime(DATETIME_FMT)
    }


def test_movie_count_queries(movie, session):
    pk = movie.id

    with count_queries(session.connection()) as queries:
        client.get(f'/api/v1/content/movies/{pk}/')

    assert len(queries) == 5


def test_movie_no_content():
    response = client.get('/api/v1/content/movies/1/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Not found',
        'error_code': ErrorCodeEnum.not_found
    }


def test_movies(movie):
    response = client.get('/api/v1/content/movies/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_movies_count_queries(session):
    MovieFactory.create_batch(10, content=ContentFactory(countries=2, genres=2, actors=2, directors=2))

    with count_queries(session.connection()) as queries:
        client.get('/api/v1/content/movies/')

    assert len(queries) == 5


def test_movies_no_content():
    response = client.get('/api/v1/content/movies/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_movies_pagination():
    MovieFactory.create_batch(10, content=ContentFactory(countries=2, genres=2, actors=2, directors=2))

    response = client.get('/api/v1/content/movies/?page=1&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids1 = {movie['id'] for movie in response.json()}

    response = client.get('/api/v1/content/movies/?page=2&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids2 = {movie['id'] for movie in response.json()}

    assert ids1 & ids2 == set()

    response = client.get('/api/v1/content/movies/?page=1&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10

    response = client.get('/api/v1/content/movies/?page=2&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
