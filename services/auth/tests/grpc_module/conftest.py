import pytest
from grpc_module.interceptors import ExceptionIntercepter
from grpc_module.service import AuthorizationService
from pytest_factoryboy import register
from tests.auth.factories import UserProfileFactory

register(UserProfileFactory, 'user', is_active=True)
register(UserProfileFactory, 'user1')


@pytest.fixture
def service():
    return AuthorizationService()


@pytest.fixture
def interceptor():
    return ExceptionIntercepter()
