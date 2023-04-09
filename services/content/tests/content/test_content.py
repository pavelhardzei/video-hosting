from unittest.mock import ANY

import pytest
from base.schemas.enums import ErrorCodeEnum
from base.utils.consts import DATETIME_FMT
from content.schemas.enums import MediaContentTypeEnum
from fastapi import status
from tests import client
from tests.content import factories
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
        'source': movie.media.source,
        'preview': movie.media.preview,
        'duration': movie.media.duration,
        'created_at': movie.media.created_at.strftime(DATETIME_FMT)
    }


def test_movie_count_queries(movie, session):
    pk = movie.id

    with count_queries(session.connection()) as queries:
        response = client.get(f'/api/v1/content/movies/{pk}/')

    assert response.status_code == status.HTTP_200_OK
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
    factories.MovieFactory.create_batch(10)

    with count_queries(session.connection()) as queries:
        response = client.get('/api/v1/content/movies/')

    assert response.status_code == status.HTTP_200_OK
    assert len(queries) == 5


def test_movies_no_content():
    response = client.get('/api/v1/content/movies/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_movies_pagination():
    factories.MovieFactory.create_batch(10)

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


@pytest.mark.parametrize(
    'params,output_len,queries_count',
    [
        ['?content__title__ilike=Man', 2, 5],
        ['?content__description__ilike=Marvel', 1, 5],
        ['?content__year=2001', 1, 5],
        ['?content__year__gte=2007', 3, 5],
        ['?content__year__lte=2007', 1, 5],
        ['?content__age_limit__lt=10', 0, 1],
        ['?content__age_limit__gte=10', 4, 5],
        ['?content__imdb_rating__gte=9.4', 1, 5],
        ['?content__kinopoisk_rating__gte=9', 2, 5],
        ['?media__duration__gte=2000', 3, 5],
        ['?media__duration__lte=2000', 2, 5],
        ['?country__name__in=Australia,Spain', 3, 5],
        ['?director__name__in=Steven Soderbergh,Hayao Miyazaki,Quentin Tarantino', 4, 5],
        ['?actor__name__in=Tom Cruise', 2, 5],
        ['?genre__name__in=Horror,Drama', 2, 5],
        ['?director__name__in=Steven Soderbergh,Hayao Miyazaki&actor__name__in=Tom Cruise', 1, 5],
        ['?content__year__gte=2007&content__age_limit__lt=18&actor__name__in=Tom Hanks', 1, 5],
        ['?content__kinopoisk_rating__gte=9&genre__name__in=Horror', 0, 1],
    ]
)
def test_movies_filters(session, movies, params, output_len, queries_count):
    with count_queries(session.connection()) as queries:
        response = client.get(f'/api/v1/content/movies/{params}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == output_len
    assert len(queries) == queries_count


@pytest.mark.parametrize(
    'params,correct_ordering_ids',
    [
        ['?content__order_by=year', (3, 1, 2, 0)],
        ['?content__order_by=age_limit,year', (0, 2, 3, 1)],
        ['?content__order_by=-year&media__order_by=-duration', (2, 3, 1, 0)],
    ]
)
def test_movies_order_by(session, movies, params, correct_ordering_ids):
    initial_ordering_ids = [movie.id for movie in movies]
    with count_queries(session.connection()) as queries:
        response = client.get(f'/api/v1/content/movies/{params}')
    assert response.status_code == status.HTTP_200_OK
    assert len(queries) == 5

    response_ordering_ids = [item['id'] for item in response.json()]
    assert response_ordering_ids == [initial_ordering_ids[i] for i in correct_ordering_ids]


def test_serial():
    serial = factories.SerialFactory(
        create_seasons=1,
        content=factories.ContentFactory(create_countries=1, create_genres=1, create_actors=1, create_directors=1),
        create_seasons__content=factories.ContentFactory(
            create_countries=1, create_genres=1, create_actors=1, create_directors=1
        ),
        create_seasons__create_episodes=1,
        create_seasons__create_episodes__content=factories.ContentFactory(
            create_countries=1, create_genres=1, create_actors=1, create_directors=1
        ),
    )
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
        response = client.get(f'/api/v1/content/serials/{pk}/')

    assert response.status_code == status.HTTP_200_OK
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
    ''' Short, i.e. do not fetch seasons '''

    factories.SerialFactory.create_batch(2)

    with count_queries(session.connection()) as queries:
        response = client.get('/api/v1/content/serials/')

    assert response.status_code == status.HTTP_200_OK
    assert len(queries) == 5


def test_serials_no_content():
    response = client.get('/api/v1/content/serials/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_serials_pagination():
    factories.SerialFactory.create_batch(
        10,
        create_seasons=1,
        create_seasons__create_episodes=1,
        content=factories.ContentFactory(create_countries=1, create_genres=1, create_actors=1, create_directors=1)
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


def test_playlist(playlist):
    response = client.get(f'/api/v1/content/playlists/{playlist.id}/')
    assert response.status_code == status.HTTP_200_OK

    assert len(playlist.playlist_items) == 1
    playlist_item = playlist.playlist_items[0]

    assert response.json() == {
        'title': playlist.title,
        'description': playlist.description,
        'playlist_type': playlist.playlist_type,
        'id': ANY,
        'playlist_items': [
            {
                'id': ANY,
                'content_type': playlist_item.object.content_type,
                'title': playlist_item.object.content.title,
                'description': playlist_item.object.content.description,
                'year': playlist_item.object.content.year,
                'release_date': playlist_item.object.content.release_date.strftime(DATETIME_FMT),
                'age_limit': playlist_item.object.content.age_limit,
                'poster': playlist_item.object.content.poster,
                'background': playlist_item.object.content.background,
                'imdb_rating': playlist_item.object.content.imdb_rating,
                'imdb_vote_count': playlist_item.object.content.imdb_vote_count,
                'kinopoisk_rating': playlist_item.object.content.kinopoisk_rating,
                'kinopoisk_vote_count': playlist_item.object.content.kinopoisk_vote_count
            }
        ]
    }


def test_playlist_count_queries(session, playlist):
    pk = playlist.id

    with count_queries(session.connection()) as queries:
        response = client.get(f'/api/v1/content/playlists/{pk}/')

    assert response.status_code == status.HTTP_200_OK
    assert len(queries) == 3


def test_playlist_no_content():
    response = client.get('/api/v1/content/playlists/1/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Not found',
        'error_code': ErrorCodeEnum.not_found
    }


def test_playlists(playlist):
    response = client.get('/api/v1/content/playlists/')
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1


def test_playlists_no_content():
    response = client.get('/api/v1/content/playlists/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_playlists_count_queries(session):
    factories.PlaylistFactory.create_batch(2, create_playlist_items=2)

    with count_queries(session.connection()) as queries:
        response = client.get('/api/v1/content/playlists/')

    assert response.status_code == status.HTTP_200_OK
    assert len(queries) == 2


def test_playlists_pagination():
    factories.PlaylistFactory.create_batch(
        10,
        create_playlist_items=1
    )

    response = client.get('/api/v1/content/playlists/?page=1&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids1 = {playlist['id'] for playlist in response.json()}

    response = client.get('/api/v1/content/playlists/?page=2&size=3')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids2 = {playlist['id'] for playlist in response.json()}

    assert ids1 & ids2 == set()

    response = client.get('/api/v1/content/playlists/?page=1&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10

    response = client.get('/api/v1/content/playlists/?page=2&size=15')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
