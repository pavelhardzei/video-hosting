from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import HTTPException, status


class BasePermission(ABC):
    @abstractmethod
    def check_object_permission(self, obj):
        pass


def check_permissions(obj, permission_classes: List[Type[BasePermission]]):
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    permissions = [permission_class() for permission_class in permission_classes]

    for permission in permissions:
        permission.check_object_permission(obj)
