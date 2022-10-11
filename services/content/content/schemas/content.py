from datetime import datetime
from typing import List, Optional

from content.schemas.details import (ContentActorsProxySchema, ContentCountriesProxySchema, ContentDirectorsProxySchema,
                                     ContentGenresProxySchema)
from content.schemas.enums import MediaContentTypeEnum
from content.schemas.mixins import FlattenMixin, OrmBaseMixin
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
