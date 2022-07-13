from base.permissions import BasePermission
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
