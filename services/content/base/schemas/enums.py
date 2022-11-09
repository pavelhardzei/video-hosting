import enum


class ErrorCodeEnum(str, enum.Enum):
    not_found = 'NotFound'
    base_error = 'BaseError'
    user_not_found = 'UserNotFound'
    already_exists = 'AlreadyExists'
