import enum


class RoleEnum(str, enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'


class EmailBaseEnum(str, enum.Enum):
    verification = 'verification'
    password_change = 'password_change'


class EmailTypeEnum(str, enum.Enum):
    verification = 'verification'
    password_change = 'password_change'
    password_changed = 'password_changed'
