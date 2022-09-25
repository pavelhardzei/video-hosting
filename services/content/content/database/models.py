from datetime import datetime

from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from content.database.mixins import ContentMixin, MediaMixin
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Media(Base, SaveDeleteDBMixin):
    title = Column(String(50), nullable=False)
    source = Column(String(100), nullable=False)
    preview = Column(String(100))
    duration = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Media(id={self.id})'


class Content(Base, SaveDeleteDBMixin):
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    year = Column(Integer, nullable=False)
    release_date = Column(DateTime)
    age_limit = Column(Integer, nullable=False)
    poster = Column(String(100), nullable=False)
    background = Column(String(100), nullable=False)

    imdb_rating = Column(Float)
    imdb_vote_count = Column(Integer)
    kinopoisk_rating = Column(Float)
    kinopoisk_vote_count = Column(Integer)

    countries = relationship('ContentCountries', back_populates='content')
    genres = relationship('ContentGenres', back_populates='content')
    actors = relationship('ContentActors', back_populates='content')
    directors = relationship('ContentDirectors', back_populates='content')

    def __repr__(self):
        return f'Content(id={self.id})'


class Movie(Base, SaveDeleteDBMixin, ContentMixin, MediaMixin):
    def __repr__(self):
        return f'Movie(id={self.id})'


class Serial(Base, SaveDeleteDBMixin, ContentMixin):
    seasons = relationship('Season', back_populates='serial')

    def __repr__(self):
        return f'Serial(id={self.id})'


class Season(Base, SaveDeleteDBMixin, ContentMixin):
    serial_id = Column(Integer, ForeignKey('serial.id', ondelete='CASCADE'))

    serial = relationship('Serial', back_populates='seasons')
    episodes = relationship('Episode', back_populates='season')

    def __repr__(self):
        return f'Season(id={self.id})'


class Episode(Base, SaveDeleteDBMixin, ContentMixin, MediaMixin):
    season_id = Column(Integer, ForeignKey('season.id', ondelete='CASCADE'))

    season = relationship('Season', back_populates='episodes')

    def __repr__(self):
        return f'Episode(id={self.id})'


class Country(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)
    abbr = Column(String(5), nullable=False)
    code = Column(Integer)


class ContentCountries(Base, SaveDeleteDBMixin, ContentMixin):
    country_id = Column(Integer, ForeignKey('country.id', ondelete='CASCADE'))

    country = relationship('Country')


class Genre(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)


class ContentGenres(Base, SaveDeleteDBMixin, ContentMixin):
    genre_id = Column(Integer, ForeignKey('genre.id', ondelete='CASCADE'))

    genre = relationship('Genre')


class Actor(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)


class ContentActors(Base, SaveDeleteDBMixin, ContentMixin):
    actor_id = Column(Integer, ForeignKey('actor.id', ondelete='CASCADE'))

    actor = relationship('Actor')


class Director(Base, SaveDeleteDBMixin):
    name = Column(String(50), nullable=False)


class ContentDirectors(Base, SaveDeleteDBMixin, ContentMixin):
    director_id = Column(Integer, ForeignKey('director.id', ondelete='CASCADE'))

    director = relationship('Director')
