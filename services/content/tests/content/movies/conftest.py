from pytest_factoryboy import LazyFixture, register
from tests.content import factories

register(factories.MediaFactory, 'media')
register(factories.ContentFactory, 'content', countries=2, genres=2, actors=2, directors=2)
register(factories.MovieFactory, 'movie', media=LazyFixture('media'), content=LazyFixture('content'))
