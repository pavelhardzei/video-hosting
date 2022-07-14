from base.permissions import BasePermission
from base.settings import settings
from fastapi import HTTPException, status


class UserActive(BasePermission):
    def check_object_permission(self, obj):
        if not obj.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User is inactive')


class UserEmailNotVerified(BasePermission):
    def check_object_permission(self, obj):
        if obj.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Email is already verified')


class UserEmailReady(BasePermission):
    def check_object_permission(self, obj):
        if not (obj.security.email_sent_time is None or obj.security.is_resend_ready):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'You can resend email in {settings.email_resend_timeout_seconds} seconds')


class UserTokenValid(BasePermission):
    def __init__(self, token):
        self.token = token

    def check_object_permission(self, obj):
        if not obj.security.check_token(self.token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Token is invalid or expired')
