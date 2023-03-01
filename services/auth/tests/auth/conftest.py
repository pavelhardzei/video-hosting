from pytest_factoryboy import register
from tests.auth.factories import UserProfileFactory

register(UserProfileFactory, 'user1')
