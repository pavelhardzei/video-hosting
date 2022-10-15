import factory
from content.database import models
from faker import Faker

fake = Faker()


class MediaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Media
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    title = fake.word()
    source = fake.uri()
    preview = fake.image_url()
    duration = fake.pyint(min_value=60, max_value=180)
    created_at = fake.date_time()


class ContentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Content
        sqlalchemy_session_persistence = 'commit'

    title = fake.word()
    description = fake.sentence(nb_words=10)
    year = fake.year()
    release_date = fake.date()
    age_limit = fake.pyint(max_value=18)
    poster = fake.image_url()
    background = fake.image_url()

    imdb_rating = fake.pyfloat(positive=True, max_value=10, right_digits=2)
    imdb_vote_count = fake.pyint(max_value=1000)
    kinopoisk_rating = fake.pyfloat(positive=True, max_value=10, right_digits=2)
    kinopoisk_vote_count = fake.pyint(max_value=1000)

    @factory.post_generation
    def countries(self, create, value, **kwargs):
        value = value if value else 0
        ContentCountriesFactory.create_batch(size=value, country=CountryFactory(), content=self, **kwargs)

    @factory.post_generation
    def genres(self, create, value, **kwargs):
        value = value if value else 0
        ContentGenresFactory.create_batch(size=value, genre=GenreFactory(), content=self, **kwargs)

    @factory.post_generation
    def actors(self, create, value, **kwargs):
        value = value if value else 0
        ContentActorsFactory.create_batch(size=value, actor=ActorFactory(), content=self, **kwargs)

    @factory.post_generation
    def directors(self, create, value, **kwargs):
        value = value if value else 0
        ContentDirectorsFactory.create_batch(size=value, director=DirectorFactory(), content=self, **kwargs)


class MovieFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Movie
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)
    media = factory.SubFactory(MediaFactory)


class SerialFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Serial
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)

    @factory.post_generation
    def seasons(self, create, value, **kwargs):
        value = value if value else 0
        episodes = kwargs.pop('episodes', 1)
        SeasonFactory.create_batch(
            size=value,
            serial=self,
            content=ContentFactory(countries=1, genres=1, actors=1, directors=1),
            episodes=episodes,
            **kwargs
        )


class SeasonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Season
        sqlalchemy_session_persistence = 'commit'

    serial = factory.SubFactory(SerialFactory)
    content = factory.SubFactory(ContentFactory)

    @factory.post_generation
    def episodes(self, create, value, **kwargs):
        value = value if value else 0
        EpisodeFactory.create_batch(
            size=value,
            season=self,
            content=ContentFactory(countries=1, genres=1, actors=1, directors=1),
            **kwargs
        )


class EpisodeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Episode
        sqlalchemy_session_persistence = 'commit'

    season = factory.SubFactory(SeasonFactory)
    content = factory.SubFactory(ContentFactory)
    media = factory.SubFactory(MediaFactory)


class CountryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Country
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    name = fake.country()
    abbr = fake.country_code()
    code = factory.Sequence(lambda code: code)


class GenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Genre
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    name = fake.word()


class ActorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Actor
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    name = fake.word()


class DirectorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Director
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda pk: pk)
    name = fake.word()


class ContentCountriesFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ContentCountries
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)
    country = factory.SubFactory(CountryFactory)


class ContentGenresFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ContentGenres
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)
    genre = factory.SubFactory(MediaFactory)


class ContentActorsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ContentActors
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)
    actor = factory.SubFactory(ActorFactory)


class ContentDirectorsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ContentDirectors
        sqlalchemy_session_persistence = 'commit'

    content = factory.SubFactory(ContentFactory)
    director = factory.SubFactory(DirectorFactory)
