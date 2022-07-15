from typing import Union

from auth.schemas.enums import EmailBaseEnum, RoleEnum
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
    username: Union[str, None] = None


class UserPasswordUpdateSchema(BaseModel):
    new_password: str
    token: str


class TokenSchema(BaseModel):
    access_token: str


class EmailSchema(BaseModel):
    email: EmailStr
    email_type: EmailBaseEnum


class DetailSchema(BaseModel):
    detail: str
