from auth.models import UserProfile
from base.permissions import BasePermission
from base.schemas.enums import ErrorCodeEnum
from base.settings import settings
from fastapi import HTTPException, status


class UserActive(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User is inactive',
                                headers={'Error-Code': ErrorCodeEnum.user_inactive})


class UserEmailNotVerified(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if obj.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Email is already verified',
                                headers={'Error-Code': ErrorCodeEnum.already_verified})


class UserEmailReady(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if not (obj.security.email_sent_time is None or obj.security.is_resend_ready):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'You can resend email in {settings.email_resend_timeout_seconds} seconds',
                                headers={'Error-Code': ErrorCodeEnum.timeout_error})


class UserAccessTokenValid(BasePermission):
    def __init__(self, token: str):
        self.token = token

    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.security.check_access_token(self.token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Token is invalid or expired',
                                headers={'Error-Code': ErrorCodeEnum.invalid_token})


class UserSecondaryTokenValid(BasePermission):
    def __init__(self, token: str):
        self.token = token

    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.security.check_secondary_token(self.token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Token is invalid or expired',
                                headers={'Error-Code': ErrorCodeEnum.invalid_token})
