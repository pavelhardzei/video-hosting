import enum
from typing import Union

from pydantic import BaseModel, EmailStr


class UserProfileBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserProfileCreateSchema(UserProfileBaseSchema):
    password: str


class RoleEnum(str, enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'


class UserProfileSchema(UserProfileBaseSchema):
    id: int
    is_active: bool
    role: RoleEnum

    class Config:
        orm_mode = True


class UserProfileUpdateSchema(UserProfileBaseSchema):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class EmailVerificationSchema(BaseModel):
    id: int
    token: str


class DetailSchema(BaseModel):
    detail: str
