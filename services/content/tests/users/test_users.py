from unittest.mock import ANY, patch

from base.schemas.enums import ErrorCodeEnum
from base.utils.consts import DATETIME_FMT
from content.schemas.enums import MediaContentTypeEnum
from fastapi import status
from tests import client
from tests.users.factories import UserLibraryFactory
from tests.utils import count_queries
from users.database.models import UserLibrary
from users.schemas.enums import LibraryTypeEnum, ObjectTypeEnum


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_get_library(user_library, *args):
    response = client.get(
        f'/api/v1/users/me/library/{user_library.library_type}/',
        headers={'Authorization': 'Bearer Token'}
    )

    assert response.status_code == status.HTTP_200_OK

    movie = user_library.object
    assert response.json() == [
        {
            'library_type': user_library.library_type,
            'offset': user_library.offset,
            'id': user_library.id,
            'user_id': 1,
            'created_at': ANY,
            'object': {
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
        }
    ]


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_get_library_count_queries(session, *args):
    UserLibraryFactory.create_batch(3, user_id=1, library_type=LibraryTypeEnum.watch_later)

    with count_queries(session.connection()) as queries:
        client.get(
            f'/api/v1/users/me/library/{LibraryTypeEnum.watch_later}/',
            headers={'Authorization': 'Bearer Token'}
        )

    assert len(queries) == 16


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_create_library(movie, session, *args):
    assert session.query(UserLibrary).count() == 0

    request = {
        'library_type': LibraryTypeEnum.favorite,
        'object_type': ObjectTypeEnum.movie,
        'object_id': movie.id
    }

    response = client.post('/api/v1/users/me/library/', json=request, headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['user_id'] == 1
    assert session.query(UserLibrary).count() == 1


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_patch_library(user_library, *args):
    request = {'offset': 30}
    response = client.patch(f'/api/v1/users/me/library/{user_library.id}/', json=request,
                            headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['offset'] == 30


@patch('users.dependences.authorize', lambda *args, **kwargs: 0)
def test_patch_library_not_found(user_library, *args):
    request = {'offset': 30}
    response = client.patch(f'/api/v1/users/me/library/{user_library.id}/', json=request,
                            headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Not found', 'error_code': ErrorCodeEnum.not_found}


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_delete_library(user_library, *args):
    response = client.delete(f'/api/v1/users/me/library/{user_library.id}/', headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_204_NO_CONTENT


@patch('users.dependences.authorize', lambda *args, **kwargs: 0)
def test_delete_library_not_found(user_library, *args):
    response = client.delete(f'/api/v1/users/me/library/{user_library.id}/', headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Not found', 'error_code': ErrorCodeEnum.not_found}


@patch('users.dependences.authorize', lambda *args, **kwargs: 1)
def test_user_library_pagination():
    UserLibraryFactory.create_batch(10, user_id=1, library_type=LibraryTypeEnum.watch_later)

    response = client.get(
        f'/api/v1/users/me/library/{LibraryTypeEnum.watch_later}/?page=1&size=3',
        headers={'Authorization': 'Bearer Token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids1 = {library['id'] for library in response.json()}

    response = client.get(
        f'/api/v1/users/me/library/{LibraryTypeEnum.watch_later}/?page=2&size=3',
        headers={'Authorization': 'Bearer Token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    ids2 = {library['id'] for library in response.json()}

    assert ids1 & ids2 == set()

    response = client.get(
        f'/api/v1/users/me/library/{LibraryTypeEnum.watch_later}/?page=1&size=15',
        headers={'Authorization': 'Bearer Token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10

    response = client.get(
        f'/api/v1/users/me/library/{LibraryTypeEnum.watch_later}/?page=2&size=15',
        headers={'Authorization': 'Bearer Token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0