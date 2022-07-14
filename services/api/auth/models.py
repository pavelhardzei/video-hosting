import enum
from datetime import datetime, timedelta

from auth import utils
from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from base.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class UserProfile(Base, SaveDeleteDBMixin):
    __tablename__ = 'user_profile'

    class RoleEnum(str, enum.Enum):
        admin = 'admin'
        moderator = 'moderator'
        viewer = 'viewer'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)
    password = Column(String(72), nullable=False)

    security = relationship('UserSecurity', back_populates='user', uselist=False, cascade='all, delete')

    def set_password(self, plain_password):
        self.password = utils.pwd_context.hash(plain_password)

    def check_password(self, plain_password):
        return utils.pwd_context.verify(plain_password, self.password)

    def __repr__(self):
        return f'UserProfile(id={self.id}, email={self.email}, is_active={self.is_active})'


class UserSecurity(Base, SaveDeleteDBMixin):
    __tablename__ = 'user_security'

    id = Column(Integer, ForeignKey('user_profile.id', ondelete='CASCADE'), primary_key=True)
    token = Column(String(150), default=lambda context:
                   utils.create_access_token({'id': context.get_current_parameters().get('id')}))
    email_sent_time = Column(DateTime)

    user = relationship('UserProfile', back_populates='security')

    @property
    def is_resend_ready(self):
        return datetime.utcnow() > self.email_sent_time + timedelta(seconds=settings.email_resend_timeout_seconds)

    def check_token(self, token):
        return self.token == token

    def __repr__(self):
        return f'UserSecurity(id={self.id})'
