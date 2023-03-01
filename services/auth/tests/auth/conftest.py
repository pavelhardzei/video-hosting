from pytest_factoryboy import register
from tests.auth.factories import UserProfileFactory

register(UserProfileFactory, 'user', is_active=True)
register(UserProfileFactory, 'user1')
