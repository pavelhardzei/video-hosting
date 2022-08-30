from typing import Any, Dict, Optional

from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from base.settings import settings
from fastapi import status


class InvalidCredentialsException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.invalid_credentials,
                 detail: Any = 'Incorrect email or password',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class InvalidTokenException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.invalid_token,
                 detail: Any = 'Token is invalid or expired',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class TokenExpiredException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.token_expired,
                 detail: Any = 'Token is expired',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class AccessTokenExpiredException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.access_token_expired,
                 detail: Any = 'Access token is expired',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class UserInactiveException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.user_inactive,
                 detail: Any = 'User is inactive',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class AlreadyVerifiedException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.already_verified,
                 detail: Any = 'Email is already verified',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class TimeoutErrorException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.timeout_error,
                 detail: Any = f'You can resend email in {settings.email_resend_timeout_seconds} seconds',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)
