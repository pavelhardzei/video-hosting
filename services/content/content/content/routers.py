from typing import Annotated

from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from base.utils.pagination import PaginationParams
from content.content.filters import MovieFilter
from content.database.models import (Actor, Content, ContentActors, ContentCountries, ContentDirectors, ContentGenres,
                                     Country, Director, Genre, Movie, Playlist, PlaylistItem, Serial)
from content.schemas.content import (MovieListSchema, MovieSchema, PlaylistListSchema, PlaylistSchema, SerialSchema,
                                     SerialShortListSchema)
from dark_utils.fastapi.filters import FilterDepends
from dark_utils.sqlalchemy_utils import attach_relationships
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, contains_eager, joinedload, selectinload, subqueryload

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
def movies(
    params: Annotated[PaginationParams, Depends()],
    session: Annotated[Session, Depends(session_dependency)],
    movie_filter: Annotated[MovieFilter, FilterDepends(MovieFilter)]
):
    movies = (
        session.query(Movie).join(Movie.content)
        .outerjoin(ContentCountries).outerjoin(Country)
        .outerjoin(ContentGenres).outerjoin(Genre)
        .outerjoin(ContentActors).outerjoin(Actor)
        .outerjoin(ContentDirectors).outerjoin(Director)
        .options(contains_eager(Movie.content).options(
            selectinload(Content.countries),
            selectinload(Content.genres),
            selectinload(Content.actors),
            selectinload(Content.directors))
        ).distinct()
    )

    movies = movie_filter.filter(movies)
    movies = movie_filter.sort(movies)

    movies = params.paginate(movies, Movie.id)

    return movies.all()


@movies_router.get(
    '/{id}/',
    response_model=MovieSchema,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}}
)
def movie(id: int, session: Session = Depends(session_dependency)):
    movie = session.query(Movie).filter(Movie.id == id).first()
    check_permissions(movie, [])

    return movie


@serials_router.get('/', response_model=SerialShortListSchema)
def serials(params: PaginationParams = Depends(), session: Session = Depends(session_dependency)):
    serials = session.query(Serial).options(joinedload(Serial.content).options(
        subqueryload(Content.countries),
        subqueryload(Content.genres),
        subqueryload(Content.actors),
        subqueryload(Content.directors))
    )
    serials = params.paginate(serials, Serial.id)

    return serials.all()


@serials_router.get('/{id}/', response_model=SerialSchema,
                    responses={status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}})
def serial(id: int, session: Session = Depends(session_dependency)):
    serial = session.query(Serial).options(subqueryload(Serial.seasons)).filter(Serial.id == id).first()
    check_permissions(serial, [])

    return serial


@playlists_router.get('/', response_model=PlaylistListSchema)
def playlists(params: PaginationParams = Depends(), session: Session = Depends(session_dependency)):
    attach_relationships(PlaylistItem, [Movie, Serial])

    playlists = session.query(Playlist).options(
        subqueryload(Playlist.playlist_items).options(
            joinedload(PlaylistItem._object_movie),
            joinedload(PlaylistItem._object_serial)
        )
    )
    playlists = params.paginate(playlists, Playlist.id)

    return playlists.all()


@playlists_router.get('/{id}/', response_model=PlaylistSchema)
def playlist(id: int, session: Session = Depends(session_dependency)):
    playlist = session.query(Playlist).options(subqueryload(Playlist.playlist_items)).filter(Playlist.id == id).first()
    check_permissions(playlist, [])

    return playlist
