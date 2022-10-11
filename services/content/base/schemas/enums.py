import enum


class ErrorCodeEnum(str, enum.Enum):
    not_found = 'NotFound'
    base_error = 'BaseError'
    already_exists = 'AlreadyExists'
