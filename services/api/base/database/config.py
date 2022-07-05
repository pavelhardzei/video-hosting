from base.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(settings.sqlalchemy_database_url, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
