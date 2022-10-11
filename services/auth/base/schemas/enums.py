import enum


class ErrorCodeEnum(str, enum.Enum):
    base_error = 'BaseError'
    invalid_credentials = 'InvalidCredentials'
    user_not_found = 'UserNotFound'
    already_exists = 'AlreadyExists'
    invalid_token = 'InvalidToken'
    token_expired = 'TokenExpired'
    access_token_expired = 'AccessTokenExpired'
    refresh_token_not_found = 'RefreshTokenNotFound'
    user_inactive = 'UserInactive'
    already_verified = 'AlreadyVerified'
    timeout_error = 'TimeoutError'
