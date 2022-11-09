from pathlib import Path

from pydantic import BaseSettings

PROJ_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str

    grpc_server: str

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
