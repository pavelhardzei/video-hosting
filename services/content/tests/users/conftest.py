from pytest_factoryboy import LazyFixture, register
from tests.content import factories
from tests.users.factories import UserLibraryFactory

register(factories.MediaFactory, 'media')
register(factories.ContentFactory, 'content', create_countries=1, create_genres=1, create_actors=1, create_directors=1)
register(factories.MovieFactory, 'movie', media=LazyFixture('media'), content=LazyFixture('content'))

register(UserLibraryFactory, 'user_library', user_id=1, object=LazyFixture('movie'))
