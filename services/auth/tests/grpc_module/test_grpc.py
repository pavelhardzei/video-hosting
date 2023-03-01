from unittest.mock import MagicMock

import pytest
from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from grpc_module.proto.authorization_pb2 import AuthorizationRequest


def test_service(service, user):
    request = AuthorizationRequest(access_token=user.security.access_token)
    response = service.authorize(request, None)

    assert response.id == user.id


def test_service_invalid_token(service, interceptor):
    request = AuthorizationRequest(access_token='invalid token')

    with pytest.raises(HTTPExceptionWithCode) as e:
        interceptor.intercept(service.authorize, request, context=MagicMock())

    assert e.value.error_code == ErrorCodeEnum.invalid_token
