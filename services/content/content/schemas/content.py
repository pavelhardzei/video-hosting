from datetime import datetime
from typing import List, Optional, Union

from base.mixins.schemas import FlattenMixin, OrmBaseMixin
from content.schemas.details import (ContentActorsProxySchema, ContentCountriesProxySchema, ContentDirectorsProxySchema,
                                     ContentGenresProxySchema)
from content.schemas.enums import MediaContentTypeEnum, PlaylistTypeEnum
from pydantic import BaseModel, Field


# BASE
class MediaBaseSchema(BaseModel):
    source: str
    preview: Optional[str]
    duration: Optional[int]


class MediaSchema(OrmBaseMixin, MediaBaseSchema):
    created_at: Optional[datetime] = None


class ContentBaseSchema(BaseModel):
    title: str
    description: str
    year: int
    release_date: Optional[datetime] = None
    age_limit: int
    poster: str
    background: str

    imdb_rating: Optional[float] = None
    imdb_vote_count: Optional[int] = None
    kinopoisk_rating: Optional[float] = None
    kinopoisk_vote_count: Optional[int] = None


class ContentSchema(OrmBaseMixin, ContentBaseSchema):
    countries: List[ContentCountriesProxySchema]
    genres: List[ContentGenresProxySchema]
    actors: List[ContentActorsProxySchema]
    directors: List[ContentDirectorsProxySchema]


# MOVIES
class MovieBaseSchema(BaseModel):
    pass


class MovieSchema(OrmBaseMixin, FlattenMixin, MovieBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentSchema = Field(flatten=True)
    media: MediaSchema = Field(flatten=True)


class MovieListSchema(BaseModel):
    __root__: List[MovieSchema]


# SERIALS
class EpisodeBaseSchema(BaseModel):
    pass


class EpisodeSchema(OrmBaseMixin, FlattenMixin, EpisodeBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentSchema = Field(flatten=True)
    media: MediaSchema = Field(flatten=True)


class SeasonBaseSchema(BaseModel):
    pass


class SeasonSchema(OrmBaseMixin, FlattenMixin, SeasonBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentSchema = Field(flatten=True)

    episodes: List[EpisodeSchema]


class SerialBaseSchema(BaseModel):
    pass


class SerialShortSchema(OrmBaseMixin, FlattenMixin, SerialBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentSchema = Field(flatten=True)


class SerialShortListSchema(BaseModel):
    __root__: List[SerialShortSchema]


class SerialSchema(SerialShortSchema):
    seasons: List[SeasonSchema]


class SerialListSchema(BaseModel):
    __root__: List[SerialSchema]


# PLAYLISTS
class ContentForPlaylistSchema(OrmBaseMixin, ContentBaseSchema):
    pass


class MovieForPlaylistSchema(OrmBaseMixin, FlattenMixin, MovieBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentForPlaylistSchema = Field(flatten=True)


class SerialForPlaylistSchema(OrmBaseMixin, FlattenMixin, SerialBaseSchema):
    id: int
    content_type: MediaContentTypeEnum
    content: ContentForPlaylistSchema = Field(flatten=True)


class PlaylistItemBaseSchema(BaseModel):
    pass


class PlaylistItemSchema(OrmBaseMixin, FlattenMixin, PlaylistItemBaseSchema):
    object: Union[MovieForPlaylistSchema, SerialForPlaylistSchema] = Field(flatten=True)


class PlaylistBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    playlist_type: PlaylistTypeEnum


class PlaylistSchema(OrmBaseMixin, PlaylistBaseSchema):
    id: int
    playlist_items: List[PlaylistItemSchema]


class PlaylistListSchema(BaseModel):
    __root__: List[PlaylistSchema]
