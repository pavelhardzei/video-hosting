from typing import Any, Dict, Optional

from base.schemas.enums import ErrorCodeEnum
from fastapi.exceptions import HTTPException


class HTTPExceptionWithCode(HTTPException):
    def __init__(self, status_code: int, detail: Any = None, headers: Optional[Dict[str, Any]] = None,
                 error_code: ErrorCodeEnum = ErrorCodeEnum.base_error) -> None:
        super().__init__(status_code, detail, headers)

        self.error_code = error_code


class BaseErrorException(HTTPExceptionWithCode):
    pass
