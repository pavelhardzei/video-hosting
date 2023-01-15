import pytest
from grpc_module.interceptors import ExceptionIntercepter
from grpc_module.service import AuthorizationService


@pytest.fixture
def service():
    return AuthorizationService()


@pytest.fixture
def interceptor():
    return ExceptionIntercepter()
