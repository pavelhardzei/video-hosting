import enum


class RoleEnum(str, enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    viewer = 'viewer'


class ConfirmationEmailBasedEnum(str, enum.Enum):
    verification = 'verification'
    password_change = 'password_change'


class ConfirmationTokenBasedEnum(str, enum.Enum):
    account_deletion = 'account_deletion'


class ConfirmationTypeEnum(str, enum.Enum):
    verification = 'verification'
    password_change = 'password_change'
    password_changed = 'password_changed'
    account_deletion = 'account_deletion'
