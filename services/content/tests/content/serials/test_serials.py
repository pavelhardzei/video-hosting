from unittest.mock import ANY

from base.schemas.enums import ErrorCodeEnum
from base.utils.consts import DATETIME_FMT
from content.schemas.enums import MediaContentTypeEnum
from fastapi import status
from tests import client
from tests.content.factories import ContentFactory, SerialFactory
from tests.utils import count_queries


def test_serial(serial):
    response = client.get(f'/api/v1/content/serials/{serial.id}/')

    assert len(serial.seasons) == 1
    season = serial.seasons[0]

    assert len(season.episodes) == 1
    episode = season.episodes[0]

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'content_type': MediaContentTypeEnum.serial,
        'id': serial.id,
        'title': serial.content.title,
        'description': serial.content.description,
        'year': serial.content.year,
        'release_date': serial.content.release_date.strftime(DATETIME_FMT),
        'age_limit': serial.content.age_limit,
        'poster': serial.content.poster,
        'background': serial.content.background,
        'imdb_rating': serial.content.imdb_rating,
        'imdb_vote_count': serial.content.imdb_vote_count,
        'kinopoisk_rating': serial.content.kinopoisk_rating,
        'kinopoisk_vote_count': serial.content.kinopoisk_vote_count,
        'countries': [
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
            }
        ],
        'actors': [
            {
                'name': ANY,
                'id': ANY
            }
        ],
        'directors': [
            {
                'name': ANY,
                'id': ANY
            }
        ],
        'seasons': [
            {
                'content_type': MediaContentTypeEnum.season,
                'id': season.id,
                'title': season.content.title,
                'description': season.content.description,
                'year': season.content.year,
                'release_date': season.content.release_date.strftime(DATETIME_FMT),
                'age_limit': season.content.age_limit,
                'poster': season.content.poster,
                'background': season.content.background,
                'imdb_rating': season.content.imdb_rating,
                'imdb_vote_count': season.content.imdb_vote_count,
                'kinopoisk_rating': season.content.kinopoisk_rating,
                'kinopoisk_vote_count': season.content.kinopoisk_vote_count,
                'countries': [
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
                    }
                ],
                'actors': [
                    {
                        'name': ANY,
                        'id': ANY
                    }
                ],
                'directors': [
                    {
                        'name': ANY,
                        'id': ANY
                    }
                ],
                'episodes': [
                    {
                        'content_type': MediaContentTypeEnum.episode,
                        'id': episode.id,
                        'title': episode.content.title,
                        'description': episode.content.description,
                        'year': episode.content.year,
                        'release_date': episode.content.release_date.strftime(DATETIME_FMT),
                        'age_limit': episode.content.age_limit,
                        'poster': episode.content.poster,
                        'background': episode.content.background,
                        'imdb_rating': episode.content.imdb_rating,
                        'imdb_vote_count': episode.content.imdb_vote_count,
                        'kinopoisk_rating': episode.content.kinopoisk_rating,
                        'kinopoisk_vote_count': episode.content.kinopoisk_vote_count,
                        'countries': [
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
                            }
                        ],
                        'actors': [
                            {
                                'name': ANY,
                                'id': ANY
                            }
                        ],
                        'directors': [
                            {
                                'name': ANY,
                                'id': ANY
                            }
                        ],
                        'source': episode.media.source,
                        'preview': episode.media.preview,
                        'duration': episode.media.duration,
                        'created_at': episode.media.created_at.strftime(DATETIME_FMT)
                    }
                ]
            }
        ]
    }


def test_serial_count_queries(serial, session):
    pk = serial.id

    with count_queries(session.connection()) as queries:
        client.get(f'/api/v1/content/serials/{pk}/')

    assert len(queries) == 15


def test_serial_no_content():
    response = client.get('/api/v1/content/serials/1/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Not found',
        'error_code': ErrorCodeEnum.not_found
    }


def test_serials(serial):
    response = client.get('/api/v1/content/serials/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_serials_count_queries(session):
    SerialFactory.create_batch(
        2,
        seasons=2,
        seasons__episodes=2,
        content=ContentFactory(countries=1, genres=1, actors=1, directors=1)
    )

    with count_queries(session.connection()) as queries:
        client.get('/api/v1/content/serials/')

    assert len(queries) == 15


def test_serials_no_content():
    response = client.get('/api/v1/content/serials/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_serials_pagination():
    SerialFactory.create_batch(
        10,
        seasons=1,
        seasons__episodes=1,
        content=ContentFactory(countries=1, genres=1, actors=1, directors=1)
    )

    response = client.get('/api/v1/content/serials/?page=1&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids1 = {serial['id'] for serial in response.json()}

    response = client.get('/api/v1/content/serials/?page=2&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids2 = {serial['id'] for serial in response.json()}

    assert ids1 & ids2 == set()

    response = client.get('/api/v1/content/serials/?page=1&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10

    response = client.get('/api/v1/content/serials/?page=2&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
