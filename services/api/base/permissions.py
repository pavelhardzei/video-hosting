from abc import ABC, abstractmethod
from typing import List

from base.schemas.enums import ErrorCodeEnum
from fastapi import HTTPException, status


class BasePermission(ABC):
    @abstractmethod
    def check_object_permission(self, obj):
        pass


def check_permissions(obj, permissions: List[BasePermission]):
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found',
                            headers={'Error-Code': ErrorCodeEnum.not_found})

    for permission in permissions:
        permission.check_object_permission(obj)
