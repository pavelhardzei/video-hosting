from typing import Optional

from content.database.models import Actor, Content, Country, Director, Genre, Media, Movie, Serial
from dark_utils.fastapi.filters import FilterDepends, with_prefix
from dark_utils.fastapi.filters.contrib.sqlalchemy import Filter


class CountryFilter(Filter):
    name__in: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Country


class DirectorFilter(Filter):
    name__in: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Director


class ActorFilter(Filter):
    name__in: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Actor


class GenreFilter(Filter):
    name__in: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Genre


class ContentFilter(Filter):
    title__ilike: Optional[str]
    description__ilike: Optional[str]
    year: Optional[int]
    year__gte: Optional[int]
    year__lte: Optional[int]
    age_limit__lt: Optional[int]
    age_limit__gte: Optional[int]
    imdb_rating__gte: Optional[float]
    kinopoisk_rating__gte: Optional[float]

    country: CountryFilter = FilterDepends(with_prefix('country', CountryFilter))
    director: DirectorFilter = FilterDepends(with_prefix('director', DirectorFilter))
    actor: ActorFilter = FilterDepends(with_prefix('actor', ActorFilter))
    genre: GenreFilter = FilterDepends(with_prefix('genre', GenreFilter))

    order_by: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Content


class MediaFilter(Filter):
    duration__gte: Optional[int]
    duration__lte: Optional[int]

    order_by: Optional[list[str]]

    class Constants(Filter.Constants):
        model = Media


class MovieFilter(Filter):
    content: ContentFilter = FilterDepends(with_prefix('content', ContentFilter))
    media: MediaFilter = FilterDepends(with_prefix('media', MediaFilter))

    class Constants(Filter.Constants):
        model = Movie


class SerialFilter(Filter):
    content: ContentFilter = FilterDepends(with_prefix('content', ContentFilter))

    class Constants(Filter.Constants):
        model = Serial
