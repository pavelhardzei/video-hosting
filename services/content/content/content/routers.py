from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from base.utils.pagination import Params, paginate
from content.database.models import Movie, Playlist, Serial
from content.schemas.content import (MovieListSchema, MovieSchema, PlaylistListSchema, PlaylistSchema, SerialSchema,
                                     SerialShortListSchema)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, subqueryload

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
def movies(params: Params = Depends(), session: Session = Depends(session_dependency)):
    movies = session.query(Movie).order_by(Movie.id)

    return paginate(movies, params)


@movies_router.get('/{id}/', response_model=MovieSchema,
                   responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def movie(id: int, session: Session = Depends(session_dependency)):
    movie = session.query(Movie).filter(Movie.id == id).first()
    check_permissions(movie, [])

    return movie


@serials_router.get('/', response_model=SerialShortListSchema)
def serials(params: Params = Depends(), session: Session = Depends(session_dependency)):
    serials = session.query(Serial).order_by(Serial.id)

    return paginate(serials, params)


@serials_router.get('/{id}/', response_model=SerialSchema,
                    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def serial(id: int, session: Session = Depends(session_dependency)):
    serial = session.query(Serial).options(subqueryload(Serial.seasons)).filter(Serial.id == id).first()
    check_permissions(serial, [])

    return serial


@playlists_router.get('/', response_model=PlaylistListSchema)
def playlists(params: Params = Depends(), session: Session = Depends(session_dependency)):
    playlists = session.query(Playlist).options(subqueryload(Playlist.playlist_items)).order_by(Playlist.id)

    return paginate(playlists, params)


@playlists_router.get('/{id}/', response_model=PlaylistSchema)
def playlist(id: int, session: Session = Depends(session_dependency)):
    playlist = session.query(Playlist).options(subqueryload(Playlist.playlist_items)).filter(Playlist.id == id).first()
    check_permissions(playlist, [])

    return playlist
