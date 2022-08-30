from typing import Optional

from auth.schemas.enums import ConfirmationEmailBasedEnum, ConfirmationTokenBasedEnum, RoleEnum
from pydantic import BaseModel, EmailStr


class UserProfileBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserProfileCreateSchema(UserProfileBaseSchema):
    password: str


class UserProfileSchema(UserProfileBaseSchema):
    id: int
    is_active: bool
    role: RoleEnum

    class Config:
        orm_mode = True


class UserProfileUpdateSchema(BaseModel):
    username: Optional[str] = None


class UserPasswordUpdateSchema(BaseModel):
    new_password: str
    token: str


class AccessTokenSchema(BaseModel):
    access_token: str


class UserTokenSchema(BaseModel):
    access_token: Optional[str] = None
    user: UserProfileSchema


class TokenSchema(BaseModel):
    token: str


class ConfirmationEmailBasedSchema(BaseModel):
    email: EmailStr
    email_type: ConfirmationEmailBasedEnum


class ConfirmationTokenBasedSchema(BaseModel):
    email_type: ConfirmationTokenBasedEnum


class DetailSchema(BaseModel):
    detail: str
