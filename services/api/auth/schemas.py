import enum

from pydantic import BaseModel


class UserProfileBaseSchema(BaseModel):
    username: str
    email: str


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


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
