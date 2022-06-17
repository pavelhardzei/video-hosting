import enum

from base.database import Base
from sqlalchemy import Boolean, Column, Enum, Integer, String


class UserProfile(Base):
    __tablename__ = 'user_profile'

    class Type(enum.Enum):
        admin = 1
        moderator = 2
        viewer = 3

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    type = Column(Enum(Type), default=Type.viewer)

    def __repr__(self):
        return f'UserProfile(id={self.id}, email={self.email}, is_active={self.is_active})'
