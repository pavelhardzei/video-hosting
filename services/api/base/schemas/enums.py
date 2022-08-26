import enum


class ErrorCodeEnum(str, enum.Enum):
    base_error = 'BaseError'
    invalid_credentials = 'InvalidCredentials'
    not_found = 'NotFound'
    already_exists = 'AlreadyExists'
    invalid_token = 'InvalidToken'
    token_expired = 'TokenExpired'
    access_token_expired = 'AccessTokenExpired'
    user_inactive = 'UserInactive'
    already_verified = 'AlreadyVerified'
    timeout_error = 'TimeoutError'
