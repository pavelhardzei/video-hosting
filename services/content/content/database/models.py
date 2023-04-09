from datetime import datetime

from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from content.database.mixins import ContentMixin, MediaMixin
from content.schemas.enums import MediaContentTypeEnum, PlaylistItemObjectEnum, PlaylistTypeEnum
from dark_utils.sqlalchemy_utils import generic_relationship
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Media(Base, SaveDeleteDBMixin):
    title = Column(String(50), nullable=False)
    source = Column(String(200), nullable=False)
    preview = Column(String(200))
    duration = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Media(id={self.id})'


class Content(Base, SaveDeleteDBMixin):
    title = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    year = Column(Integer, nullable=False)
    release_date = Column(DateTime)
    age_limit = Column(Integer, nullable=False)
    poster = Column(String(200), nullable=False)
    background = Column(String(200), nullable=False)

    imdb_rating = Column(Float)
    imdb_vote_count = Column(Integer)
    kinopoisk_rating = Column(Float)
    kinopoisk_vote_count = Column(Integer)

    countries = relationship(
        'ContentCountries',
        back_populates='content',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )
    genres = relationship(
        'ContentGenres',
        back_populates='content',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )
    actors = relationship(
        'ContentActors',
        back_populates='content',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )
    directors = relationship(
        'ContentDirectors',
        back_populates='content',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Content(id={self.id})'


class Movie(Base, SaveDeleteDBMixin, ContentMixin, MediaMixin):
    content_type = Column(Enum(MediaContentTypeEnum), default=MediaContentTypeEnum.movie)

    def __repr__(self):
        return f'Movie(id={self.id}, content_id={self.content_id}, media_id={self.media_id})'


class Serial(Base, SaveDeleteDBMixin, ContentMixin):
    content_type = Column(Enum(MediaContentTypeEnum), default=MediaContentTypeEnum.serial)

    seasons = relationship(
        'Season',
        back_populates='serial',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Serial(id={self.id}, content_id={self.content_id})'


class Season(Base, SaveDeleteDBMixin, ContentMixin):
    content_type = Column(Enum(MediaContentTypeEnum), default=MediaContentTypeEnum.season)

    serial_id = Column(Integer, ForeignKey('serial.id', ondelete='CASCADE'), nullable=False)

    serial = relationship('Serial', back_populates='seasons')
    episodes = relationship(
        'Episode',
        back_populates='season',
        lazy='subquery',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Season(id={self.id}, serial_id={self.serial_id}, content_id={self.content_id})'


class Episode(Base, SaveDeleteDBMixin, ContentMixin, MediaMixin):
    content_type = Column(Enum(MediaContentTypeEnum), default=MediaContentTypeEnum.episode)

    season_id = Column(Integer, ForeignKey('season.id', ondelete='CASCADE'), nullable=False)

    season = relationship('Season', back_populates='episodes')

    def __repr__(self):
        return f'Episode(season_id={self.season_id}, content_id={self.content_id}, media_id={self.media_id})'


class Country(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)
    abbr = Column(String(5), nullable=False)
    code = Column(Integer)

    content_countries = relationship(
        'ContentCountries',
        back_populates='country',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Country(id={self.id}, name={self.name}, abbr={self.abbr})'


class ContentCountries(Base, SaveDeleteDBMixin, ContentMixin):
    country_id = Column(Integer, ForeignKey('country.id', ondelete='CASCADE'), nullable=False)

    country = relationship('Country', back_populates='content_countries', lazy='joined')
    content = relationship('Content', back_populates='countries')

    def __repr__(self):
        return f'ContentCountries(id={self.id}, country_id={self.country_id}, content_id={self.content_id})'


class Genre(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)

    content_genres = relationship(
        'ContentGenres',
        back_populates='genre',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Genre(id={self.id}, name={self.name})'


class ContentGenres(Base, SaveDeleteDBMixin, ContentMixin):
    genre_id = Column(Integer, ForeignKey('genre.id', ondelete='CASCADE'), nullable=False)

    genre = relationship('Genre', back_populates='content_genres', lazy='joined')
    content = relationship('Content', back_populates='genres')

    def __repr__(self):
        return f'ContentGenres(id={self.id}, genre_id={self.genre_id}, content_id={self.content_id})'


class Actor(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)

    content_actors = relationship(
        'ContentActors',
        back_populates='actor',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Actor(id={self.id}, name={self.name})'


class ContentActors(Base, SaveDeleteDBMixin, ContentMixin):
    actor_id = Column(Integer, ForeignKey('actor.id', ondelete='CASCADE'), nullable=False)

    actor = relationship('Actor', back_populates='content_actors', lazy='joined')
    content = relationship('Content', back_populates='actors')

    def __repr__(self):
        return f'ContentActors(id={self.id}, actor_id={self.actor_id}, content_id={self.content_id})'


class Director(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)

    content_directors = relationship(
        'ContentDirectors',
        back_populates='director',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )

    def __repr__(self):
        return f'Director(id={self.id}, name={self.name})'


class ContentDirectors(Base, SaveDeleteDBMixin, ContentMixin):
    director_id = Column(Integer, ForeignKey('director.id', ondelete='CASCADE'), nullable=False)

    director = relationship('Director', back_populates='content_directors', lazy='joined')
    content = relationship('Content', back_populates='directors')

    def __repr__(self):
        return f'ContentDirectors(id={self.id}, director_id={self.director_id}, content_id={self.content_id})'


class Playlist(Base, SaveDeleteDBMixin):
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    playlist_type = Column(Enum(PlaylistTypeEnum), nullable=False)

    playlist_items = relationship(
        'PlaylistItem',
        back_populates='playlist',
        passive_deletes=True,
        cascade='save-update, merge, delete'
    )


class PlaylistItem(Base, SaveDeleteDBMixin):
    __table_args__ = (UniqueConstraint('object_type', 'object_id', 'playlist_id'), )

    playlist_id = Column(Integer, ForeignKey('playlist.id', ondelete='CASCADE'), nullable=False)
    playlist = relationship('Playlist', back_populates='playlist_items')

    object_type = Column(Enum(PlaylistItemObjectEnum), nullable=False)
    object_id = Column(Integer, nullable=False)
    object = generic_relationship('object_type', 'object_id')
