from admin import exceptions
from admin.schemas.enums import RoleEnum
from base.permissions import BasePermission


class AdminUser(BasePermission):
    def check_object_permission(self, user_data: dict) -> None:
        if user_data.get('role') != RoleEnum.admin:
            raise exceptions.UserIsNotAdminException()
