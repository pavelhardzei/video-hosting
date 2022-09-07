from auth import exceptions
from auth.models import UserProfile
from base.permissions import BasePermission


class UserActive(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.is_active:
            raise exceptions.UserInactiveException()


class UserEmailNotVerified(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if obj.is_active:
            raise exceptions.AlreadyVerifiedException()


class UserEmailReady(BasePermission):
    def check_object_permission(self, obj: UserProfile) -> None:
        if not (obj.security.email_sent_time is None or obj.security.is_resend_ready):
            raise exceptions.TimeoutErrorException()


class UserAccessTokenValid(BasePermission):
    def __init__(self, token: str):
        self.token = token

    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.security.check_access_token(self.token):
            raise exceptions.InvalidTokenException()


class UserSecondaryTokenValid(BasePermission):
    def __init__(self, token: str):
        self.token = token

    def check_object_permission(self, obj: UserProfile) -> None:
        if not obj.security.check_secondary_token(self.token):
            raise exceptions.InvalidTokenException()


class UserRefreshTokenValid(BasePermission):
    def __init__(self, token: str):
        self.token = token

    def check_object_permission(self, obj: UserProfile) -> None:
        if self.token not in [item.refresh_token for item in obj.refresh_tokens]:
            raise exceptions.RefreshTokenNotFoundException()
