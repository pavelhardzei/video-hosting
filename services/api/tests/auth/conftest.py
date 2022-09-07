import pytest
from auth import utils
from pytest_factoryboy import LazyFixture, register
from tests.auth.factories import UserProfileFactory, UserRefreshTokensFactory, UserSecurityFactory

register(UserProfileFactory, 'user1')

register(UserSecurityFactory, 'user1_security', access_token=LazyFixture('user1_token'), user=LazyFixture('user1'))

register(UserRefreshTokensFactory, 'user1_refresh_token', refresh_token=LazyFixture('user1_token'),
         user=LazyFixture('user1'))


@pytest.fixture
def user1_token(user1):
    return utils.create_token({'id': user1.id})
