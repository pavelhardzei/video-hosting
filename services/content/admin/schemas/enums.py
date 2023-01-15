import enum


class RoleEnum(str, enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'
