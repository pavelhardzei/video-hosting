import pytest
from grpc_module.interceptors import ExceptionIntercepter
from grpc_module.service import AuthorizationServicer


@pytest.fixture
def service():
    return AuthorizationServicer()


@pytest.fixture
def interceptor():
    return ExceptionIntercepter()
