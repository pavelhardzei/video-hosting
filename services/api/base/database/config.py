from base.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

settings = Settings()

engine = create_engine(settings.sqlalchemy_database_url, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
