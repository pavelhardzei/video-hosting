from typing import Any, Dict, Optional

from base.schemas.enums import ErrorCodeEnum
from fastapi import status
from fastapi.exceptions import HTTPException


class HTTPExceptionWithCode(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCodeEnum,
                 detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, detail, headers)

        self.error_code = error_code


class BaseErrorException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.base_error,
                 detail: Any = None,
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class NotFoundException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_404_NOT_FOUND,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.not_found,
                 detail: Any = 'Not found',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)


class AlreadyExistsException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.already_exists,
                 detail: Any = 'Unique constraints violation',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)
