from pytest_factoryboy import LazyFixture, register
from tests.content import factories

register(factories.ContentFactory, 'content', countries=1, genres=1, actors=1, directors=1)
register(factories.SerialFactory, 'serial', seasons=1, content=LazyFixture('content'))
