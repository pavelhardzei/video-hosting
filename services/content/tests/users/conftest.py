from pytest_factoryboy import LazyFixture, register
from tests.content import factories
from tests.users.factories import UserLibraryFactory

register(factories.MediaFactory, 'media')
register(factories.ContentFactory, 'content', countries=1, genres=1, actors=1, directors=1)
register(factories.MovieFactory, 'movie', media=LazyFixture('media'), content=LazyFixture('content'))

register(UserLibraryFactory, 'user_library', user_id=1, object=LazyFixture('movie'))
