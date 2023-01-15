from typing import Any, Dict, Optional

from base.exceptions import HTTPExceptionWithCode
from base.schemas.enums import ErrorCodeEnum
from fastapi import status


class UserIsNotAdminException(HTTPExceptionWithCode):
    def __init__(self, status_code: int = status.HTTP_403_FORBIDDEN,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.user_is_not_admin,
                 detail: Any = 'User is not admin',
                 headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, error_code, detail, headers)
