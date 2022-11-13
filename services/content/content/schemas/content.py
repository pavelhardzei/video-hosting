from datetime import datetime
from typing import List, Optional

from base.mixins.schemas import FlattenMixin, OrmBaseMixin
from content.schemas.details import (ContentActorsProxySchema, ContentCountriesProxySchema, ContentDirectorsProxySchema,
                                     ContentGenresProxySchema)
from content.schemas.enums import MediaContentTypeEnum
from pydantic import BaseModel, Field


class MediaBaseSchema(BaseModel):
    source: str
    preview: str
    duration: int


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


class MovieBaseSchema(BaseModel):
    content_type: MediaContentTypeEnum = MediaContentTypeEnum.movie


class MovieSchema(OrmBaseMixin, FlattenMixin, MovieBaseSchema):
    id: int
    content: ContentSchema = Field(flatten=True)
    media: MediaSchema = Field(flatten=True)


class MovieListSchema(BaseModel):
    __root__: List[MovieSchema]


class EpisodeBaseSchema(BaseModel):
    content_type: MediaContentTypeEnum = MediaContentTypeEnum.episode


class EpisodeSchema(OrmBaseMixin, FlattenMixin, EpisodeBaseSchema):
    id: int
    content: ContentSchema = Field(flatten=True)
    media: MediaSchema = Field(flatten=True)


class SeasonBaseSchema(BaseModel):
    content_type: MediaContentTypeEnum = MediaContentTypeEnum.season


class SeasonSchema(OrmBaseMixin, FlattenMixin, SeasonBaseSchema):
    id: int
    content: ContentSchema = Field(flatten=True)

    episodes: List[EpisodeSchema]


class SerialBaseSchema(BaseModel):
    content_type: MediaContentTypeEnum = MediaContentTypeEnum.serial


class SerialSchema(OrmBaseMixin, FlattenMixin, SerialBaseSchema):
    id: int
    content: ContentSchema = Field(flatten=True)

    seasons: List[SeasonSchema]


class SerialListSchema(BaseModel):
    __root__: List[SerialSchema]
