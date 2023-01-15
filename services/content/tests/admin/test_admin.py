from unittest.mock import patch

from admin.schemas.enums import RoleEnum
from content.database.models import Playlist
from content.schemas.enums import PlaylistItemObjectEnum, PlaylistTypeEnum
from fastapi import status
from tests import client
from tests.utils import count_queries


@patch('base.utils.dependences.authorize', lambda *args, **kwargs: {'id': 1, 'role': RoleEnum.admin})
def test_create_playlist(movie, serial, session):
    assert session.query(Playlist).count() == 0

    request = {
        'title': 'Title',
        'description': 'Description',
        'playlist_type': PlaylistTypeEnum.cards,
        'playlist_items': [
            {
                'object_type': PlaylistItemObjectEnum.movie,
                'object_id': movie.id
            },
            {
                'object_type': PlaylistItemObjectEnum.serial,
                'object_id': serial.id
            }
        ]
    }

    with count_queries(session.connection()) as queries:
        response = client.post('/api/v1/admin/playlists/', json=request, headers={'Authorization': 'Bearer Token'})
    assert len(queries) == 2

    assert response.status_code == status.HTTP_201_CREATED
    assert session.query(Playlist).count() == 1
    assert len(session.query(Playlist).first().playlist_items) == 2


@patch('base.utils.dependences.authorize', lambda *args, **kwargs: {'id': 1, 'role': RoleEnum.viewer})
def test_create_playlist_not_admin(movie, session):
    assert session.query(Playlist).count() == 0

    request = {
        'title': 'Title',
        'description': 'Description',
        'playlist_type': PlaylistTypeEnum.cards,
        'playlist_items': [
            {
                'object_type': PlaylistItemObjectEnum.movie,
                'object_id': movie.id
            }
        ]
    }

    response = client.post('/api/v1/admin/playlists/', json=request, headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert session.query(Playlist).count() == 0


@patch('base.utils.dependences.authorize', lambda *args, **kwargs: {'id': 1, 'role': RoleEnum.admin})
def test_delete_playlist(playlist, session):
    assert session.query(Playlist).count() == 1

    with count_queries(session.connection()) as queries:
        response = client.delete(f'/api/v1/admin/playlists/{playlist.id}/', headers={'Authorization': 'Bearer Token'})
    len(queries) == 1

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert session.query(Playlist).count() == 0


@patch('base.utils.dependences.authorize', lambda *args, **kwargs: {'id': 1, 'role': RoleEnum.viewer})
def test_delete_playlist_not_admin(playlist, session):
    assert session.query(Playlist).count() == 1

    response = client.delete(f'/api/v1/admin/playlists/{playlist.id}/', headers={'Authorization': 'Bearer Token'})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert session.query(Playlist).count() == 1
