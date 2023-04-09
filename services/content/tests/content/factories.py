import factory
from content.database import models
from content.schemas import enums
from faker import Faker

fake = Faker()


class MediaFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Media
        sqlalchemy_session_persistence = 'commit'

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
    def create_countries(self, create, value, **kwargs):
        ContentCountriesFactory.create_batch(
            size=value if value is not None else 2, country=CountryFactory(), content=self, **kwargs
        )

    @factory.post_generation
    def create_genres(self, create, value, **kwargs):
        ContentGenresFactory.create_batch(
            size=value if value is not None else 2, genre=GenreFactory(), content=self, **kwargs
        )

    @factory.post_generation
    def create_actors(self, create, value, **kwargs):
        ContentActorsFactory.create_batch(
            size=value if value is not None else 2, actor=ActorFactory(), content=self, **kwargs
        )

    @factory.post_generation
    def create_directors(self, create, value, **kwargs):
        ContentDirectorsFactory.create_batch(
            size=value if value is not None else 2, director=DirectorFactory(), content=self, **kwargs
        )


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
    def create_seasons(self, create, value, **kwargs):
        episodes = kwargs.pop('create_episodes', 2)
        content = kwargs.pop('content', ContentFactory(
            create_countries=2, create_genres=2, create_actors=2, create_directors=2)
        )
        SeasonFactory.create_batch(
            size=value or 2,
            serial=self,
            content=content,
            create_episodes=episodes,
            **kwargs
        )


class SeasonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Season
        sqlalchemy_session_persistence = 'commit'

    serial = factory.SubFactory(SerialFactory)
    content = factory.SubFactory(ContentFactory)

    @factory.post_generation
    def create_episodes(self, create, value, **kwargs):
        content = kwargs.pop(
            'content', ContentFactory(create_countries=2, create_genres=2, create_actors=2, create_directors=2)
        )
        EpisodeFactory.create_batch(
            size=value or 2,
            season=self,
            content=content,
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

    name = fake.country()
    abbr = fake.country_code()
    code = factory.Sequence(lambda code: code)


class GenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Genre
        sqlalchemy_session_persistence = 'commit'

    name = fake.word()


class ActorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Actor
        sqlalchemy_session_persistence = 'commit'

    name = fake.word()


class DirectorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Director
        sqlalchemy_session_persistence = 'commit'

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


class PlaylistFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Playlist
        sqlalchemy_session_persistence = 'commit'

    title = fake.word()
    description = fake.sentence(nb_words=10)
    playlist_type = enums.PlaylistTypeEnum.cards

    @factory.post_generation
    def create_playlist_items(self, create, value, **kwargs):
        PlaylistItemFactory.create_batch(size=value or 2, playlist=self, **kwargs)


class PlaylistItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.PlaylistItem
        sqlalchemy_session_persistence = 'commit'

    object_type = enums.PlaylistItemObjectEnum.movie
    object_id = 1

    @factory.post_generation
    def create_object(self, create, value, **kwargs):
        self.object = MovieFactory()
        self.save()
