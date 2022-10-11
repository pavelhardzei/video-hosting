from datetime import datetime, timedelta

from auth import utils
from auth.schemas.enums import RoleEnum
from base.database.config import Base
from base.database.mixins import SaveDeleteDBMixin
from base.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class UserProfile(Base, SaveDeleteDBMixin):
    username = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)
    password = Column(String(72), nullable=False)

    security = relationship('UserSecurity', back_populates='user', lazy='joined',
                            uselist=False, cascade='all, delete')
    refresh_tokens = relationship('UserRefreshTokens', back_populates='user', cascade='all, delete')

    def set_password(self, plain_password: str) -> None:
        self.password = utils.pwd_context.hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        return utils.pwd_context.verify(plain_password, self.password)

    def create_refresh_token(self) -> str:
        if len(self.refresh_tokens) >= settings.refresh_tokens_number:
            self.refresh_tokens.sort(key=lambda obj: -obj.id)
            oldest = self.refresh_tokens.pop()
            oldest.delete()

        obj = UserRefreshTokens(user=self)
        obj.save()
        obj.refresh_token = utils.create_token({'id': obj.id, 'user_id': self.id})

        return obj.refresh_token

    def __repr__(self):
        return f'UserProfile(id={self.id}, email={self.email}, is_active={self.is_active})'


class UserSecurity(Base, SaveDeleteDBMixin):
    id = Column(Integer, ForeignKey('userprofile.id', ondelete='CASCADE'), primary_key=True)
    access_token = Column(String(150))
    secondary_token = Column(String(150), default=lambda context:
                             utils.create_token({'id': context.get_current_parameters().get('id')}))
    email_sent_time = Column(DateTime)

    user = relationship('UserProfile', back_populates='security')

    @property
    def is_resend_ready(self) -> bool:
        return datetime.utcnow() > self.email_sent_time + timedelta(seconds=settings.email_resend_timeout_seconds)

    def check_access_token(self, access_token: str) -> bool:
        return self.access_token == access_token

    def update_access_token(self) -> None:
        if self.access_token is None or utils.token_expired(self.access_token):
            self.access_token = utils.create_token({'id': self.id})

    def check_secondary_token(self, secondary_token: str) -> bool:
        return self.secondary_token == secondary_token

    def __repr__(self):
        return f'UserSecurity(id={self.id})'


class UserRefreshTokens(Base, SaveDeleteDBMixin):
    user_id = Column(Integer, ForeignKey('userprofile.id', ondelete='CASCADE'))
    refresh_token = Column(String(150))

    user = relationship('UserProfile', back_populates='refresh_tokens')

    def __repr__(self):
        return f'UserRefreshTokens(id={self.id}, user_id={self.user_id})'
