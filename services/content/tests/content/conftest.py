import pytest
from pytest_factoryboy import LazyFixture, register
from tests.content.factories import (ActorFactory, ContentActorsFactory, ContentCountriesFactory,
                                     ContentDirectorsFactory, ContentFactory, ContentGenresFactory, CountryFactory,
                                     DirectorFactory, GenreFactory, MediaFactory, MovieFactory, PlaylistFactory,
                                     SerialFactory)

register(MediaFactory, 'media')
register(ContentFactory, 'content', create_countries=1, create_genres=1, create_actors=1, create_directors=1)
register(MovieFactory, 'movie', media=LazyFixture('media'), content=LazyFixture('content'))

register(SerialFactory, 'serial', create_seasons=1, content=LazyFixture('content'))

register(PlaylistFactory, 'playlist', create_playlist_items=1)


@pytest.fixture
def countries():
    countries_ = ('USA', 'Australia', 'Spain', 'Japan', 'China')
    countries = [CountryFactory(name=name) for name in countries_]
    return countries


@pytest.fixture
def genres():
    genres_ = ('Horror', 'Adventure', 'Fantasy', 'Action', 'Drama')
    genres = [GenreFactory(name=name) for name in genres_]
    return genres


@pytest.fixture
def actors():
    actors_ = ('Tom Hanks', 'Leonardo DiCaprio', 'Harrison Ford', 'Tom Cruise', 'Will Smith')
    actors = [ActorFactory(name=name) for name in actors_]
    return actors


@pytest.fixture
def directors():
    directors_ = ('Martin Scorsese', 'Steven Soderbergh', 'Hayao Miyazaki', 'Quentin Tarantino', 'David Fincher')
    directors = [DirectorFactory(name=name) for name in directors_]
    return directors


@pytest.fixture
def content_data(countries, genres, actors, directors):
    titles = ('Man of Steel', 'Iron Man', 'Avengers', 'Harry Potter')
    descriptions = ('DC Superman', 'Marvel Tony Stark', 'Six Avengers', 'Hogwarts Legacy')
    years = (2013, 2008, 2012, 2001)
    age_limits = (10, 18, 16, 18)
    imdb_ratings = (8.6, 9.1, 8.2, 9.5)
    kinopoisk_ratings = (8.2, 9.3, 8.5, 9.1)

    contents = [
        ContentFactory(
            create_countries=0, create_genres=0, create_actors=0, create_directors=0,
            countries=[ContentCountriesFactory(country=countries[i]),
                       ContentCountriesFactory(country=countries[i + 1])],
            genres=[ContentGenresFactory(genre=genres[i]), ContentGenresFactory(genre=genres[i + 1])],
            actors=[ContentActorsFactory(actor=actors[i]), ContentActorsFactory(actor=actors[i + 1])],
            directors=[ContentDirectorsFactory(director=directors[i]),
                       ContentDirectorsFactory(director=directors[i + 1])],
            title=titles[i],
            description=descriptions[i],
            year=years[i],
            age_limit=age_limits[i],
            imdb_rating=imdb_ratings[i],
            kinopoisk_rating=kinopoisk_ratings[i]
        )
        for i in range(4)
    ]

    return contents


@pytest.fixture
def media_data():
    media_duration = (1000, 2000, 3000, 4000)
    media = [MediaFactory(duration=duration) for duration in media_duration]
    return media


@pytest.fixture
def movies(content_data, media_data):
    movies = [MovieFactory(content=content, media=media) for content, media in zip(content_data, media_data)]
    return movies
