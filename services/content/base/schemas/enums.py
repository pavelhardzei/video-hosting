import enum


class ErrorCodeEnum(str, enum.Enum):
    base_error = 'BaseError'
    not_found = 'NotFound'
    already_exists = 'AlreadyExists'
