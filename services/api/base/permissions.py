from abc import ABC, abstractmethod
from typing import Any, List

from base.schemas.enums import ErrorCodeEnum
from fastapi import HTTPException, status


class BasePermission(ABC):
    @abstractmethod
    def check_object_permission(self, obj: Any) -> None:
        pass


def check_permissions(obj: Any, permissions: List[BasePermission]) -> None:
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found',
                            headers={'Error-Code': ErrorCodeEnum.not_found})

    for permission in permissions:
        permission.check_object_permission(obj)
