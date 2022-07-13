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


class UserProfileUpdateSchema(BaseModel):
    username: Union[str, None] = None


class UserPasswordUpdateSchema(BaseModel):
    old_password: str
    new_password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class EmailVerificationSchema(BaseModel):
    id: int
    token: str


class EmailSchema(BaseModel):
    email: EmailStr


class DetailSchema(BaseModel):
    detail: str
