import os
from pathlib import Path

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    email_resend_timeout_seconds = 30

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()


class EmailSettings(BaseSettings):
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool
    MAIL_SSL: bool
    TEMPLATE_FOLDER: str = os.path.join(Path(__file__).resolve().parent.parent, 'templates')

    class Config:
        env_file_encoding = 'utf-8'


email_settings = EmailSettings()
