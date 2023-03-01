from pytest_factoryboy import LazyFixture, register
from tests.content import factories

register(factories.MediaFactory, 'media')
register(factories.ContentFactory, 'content', create_countries=1, create_genres=1, create_actors=1, create_directors=1)
register(factories.MovieFactory, 'movie', media=LazyFixture('media'), content=LazyFixture('content'))

register(factories.SerialFactory, 'serial', create_seasons=1, content=LazyFixture('content'))

register(factories.PlaylistFactory, 'playlist', create_playlist_items=1)
