from base.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

engine = create_engine(settings.sqlalchemy_database_url, future=True, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
