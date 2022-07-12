import pytest
from auth import utils
from pytest_factoryboy import LazyFixture, register
from testing.auth.factories import UserProfileFactory, UserSecurityFactory

register(UserProfileFactory, 'user1')

register(UserSecurityFactory, 'user1_security', token=LazyFixture('user1_token'), user=LazyFixture('user1'))


@pytest.fixture
def user1_token(user1):
    return utils.create_access_token({'id': user1.id})
