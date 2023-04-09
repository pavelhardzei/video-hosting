from typing import Annotated

from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from base.utils.pagination import PaginationParams
from content.content.filters import MovieFilter, SerialFilter
from content.database.models import Movie, Playlist, PlaylistItem, Serial
from content.schemas.content import (MovieListSchema, MovieSchema, PlaylistListSchema, PlaylistSchema, SerialSchema,
                                     SerialShortListSchema)
from content.utils import prefetch_content_data
from dark_utils.fastapi.filters import FilterDepends
from dark_utils.sqlalchemy_utils import attach_relationships
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, contains_eager, joinedload, selectinload

movies_router = APIRouter(
    prefix='/movies'
)
serials_router = APIRouter(
    prefix='/serials'
)
playlists_router = APIRouter(
    prefix='/playlists'
)


@movies_router.get('/', response_model=MovieListSchema)
def get_movies(
    params: Annotated[PaginationParams, Depends()],
    session: Annotated[Session, Depends(session_dependency)],
    movie_filter: Annotated[MovieFilter, FilterDepends(MovieFilter)]
):
    movies = session.query(Movie).join(Movie.media).options(contains_eager(Movie.media))
    movies = prefetch_content_data(movies)

    movies = movie_filter.filter(movies)
    movies = movie_filter.sort(movies)

    movies = params.paginate(movies, Movie.id)

    return movies.all()


@movies_router.get(
    '/{id}/',
    response_model=MovieSchema,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}}
)
def get_movie(id: int, session: Annotated[Session, Depends(session_dependency)]):
    movie = session.query(Movie).filter(Movie.id == id).first()
    check_permissions(movie, [])

    return movie


@serials_router.get('/', response_model=SerialShortListSchema)
def get_serials(
    params: Annotated[PaginationParams, Depends()],
    session: Annotated[Session, Depends(session_dependency)],
    serial_filter: Annotated[SerialFilter, FilterDepends(SerialFilter)]
):
    serials = session.query(Serial)
    serials = prefetch_content_data(serials)

    serials = serial_filter.filter(serials)
    serials = serial_filter.sort(serials)

    serials = params.paginate(serials, Serial.id)

    return serials.all()


@serials_router.get('/{id}/', response_model=SerialSchema,
                    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def get_serial(id: int, session: Annotated[Session, Depends(session_dependency)]):
    serial = session.query(Serial).options(selectinload(Serial.seasons)).filter(Serial.id == id).first()
    check_permissions(serial, [])

    return serial


@playlists_router.get('/', response_model=PlaylistListSchema)
def get_playlists(
    params: Annotated[PaginationParams, Depends()],
    session: Annotated[Session, Depends(session_dependency)]
):
    attach_relationships(PlaylistItem, [Movie, Serial])

    playlists = session.query(Playlist).options(
        selectinload(Playlist.playlist_items).options(
            joinedload(PlaylistItem._object_movie),
            joinedload(PlaylistItem._object_serial)
        )
    )
    playlists = params.paginate(playlists, Playlist.id)

    return playlists.all()


@playlists_router.get('/{id}/', response_model=PlaylistSchema)
def get_playlist(id: int, session: Annotated[Session, Depends(session_dependency)]):
    playlist = session.query(Playlist).options(selectinload(Playlist.playlist_items)).filter(Playlist.id == id).first()
    check_permissions(playlist, [])

    return playlist
