from datetime import datetime

from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from sqlalchemy import Column, DateTime, Enum, Integer, Unicode, UniqueConstraint
from sqlalchemy_utils import generic_relationship
from users.schemas.enums import LibraryTypeEnum


class UserLibrary(Base, SaveDeleteDBMixin):
    __table_args__ = (UniqueConstraint('object_type', 'object_id', 'user_id', 'list_type'), )

    object_type = Column(Unicode(255), nullable=False)
    object_id = Column(Integer, nullable=False)
    object = generic_relationship(object_type, object_id)

    user_id = Column(Integer, nullable=False)
    list_type = Column(Enum(LibraryTypeEnum), nullable=False)
    offset = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
