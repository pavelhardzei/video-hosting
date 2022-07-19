from pytest_factoryboy import register
from testing.auth.factories import UserProfileFactory

register(UserProfileFactory, 'user1', email='test1@test.com', username='test1', is_active=True)
