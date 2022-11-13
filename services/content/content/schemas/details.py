from base.mixins.schemas import FlattenMixin, OrmBaseMixin
from pydantic import BaseModel, Field


class CountryBaseSchema(BaseModel):
    name: str
    abbr: str
    code: int


class CountrySchema(OrmBaseMixin, CountryBaseSchema):
    id: int


class ContentCountriesProxySchema(OrmBaseMixin, FlattenMixin, BaseModel):
    country: CountrySchema = Field(flatten=True)


class GenreBaseSchema(BaseModel):
    name: str


class GenreSchema(OrmBaseMixin, GenreBaseSchema):
    id: int


class ContentGenresProxySchema(OrmBaseMixin, FlattenMixin, BaseModel):
    genre: GenreSchema = Field(flatten=True)


class ActorBaseSchema(BaseModel):
    name: str


class ActorSchema(OrmBaseMixin, ActorBaseSchema):
    id: int


class ContentActorsProxySchema(OrmBaseMixin, FlattenMixin, BaseModel):
    actor: ActorSchema = Field(flatten=True)


class DirectorBaseSchema(BaseModel):
    name: str


class DirectorSchema(OrmBaseMixin, DirectorBaseSchema):
    id: int


class ContentDirectorsProxySchema(OrmBaseMixin, FlattenMixin, BaseModel):
    director: DirectorSchema = Field(flatten=True)
