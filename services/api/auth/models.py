import enum

from auth.utils import pwd_context
from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from sqlalchemy import Boolean, Column, Enum, Integer, String


class UserProfile(Base, SaveDeleteDBMixin):
    __tablename__ = 'user_profile'

    class Role(enum.Enum):
        admin = 1
        moderator = 2
        viewer = 3

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.viewer)
    password = Column(String(72), nullable=False)

    def set_password(self, plain_password):
        self.password = pwd_context.hash(plain_password)

    def check_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def __repr__(self):
        return f'UserProfile(id={self.id}, email={self.email}, is_active={self.is_active})'
