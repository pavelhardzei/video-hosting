from abc import ABC, abstractmethod
from typing import Any, List

from base import exceptions


class BasePermission(ABC):
    @abstractmethod
    def check_object_permission(self, obj: Any) -> None:
        pass


def check_permissions(obj: Any, permissions: List[BasePermission]) -> None:
    if obj is None:
        raise exceptions.NotFoundException()

    for permission in permissions:
        permission.check_object_permission(obj)
