import enum


class ErrorCodeEnum(str, enum.Enum):
    base_error = 'BaseError'
    invalid_credentials = 'InvalidCredentials'
    not_found = 'NotFound'
    already_exists = 'AlreadyExists'
    invalid_token = 'InvalidToken'
    user_inactive = 'UserInactive'
    already_verified = 'AlreadyVerified'
    timeout_error = 'TimeoutError'