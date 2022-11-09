from typing import Any, Dict, Optional

from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from fastapi import status


class UserNotFoundException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.user_not_found,
                 detail: Any = 'User not found',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)
