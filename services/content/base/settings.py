from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
