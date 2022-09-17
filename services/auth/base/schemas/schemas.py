from base.schemas.enums import ErrorCodeEnum
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    detail: str
    error_code: ErrorCodeEnum
