from base.settings import settings
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base, declared_attr, scoped_session, sessionmaker


class DeclarativeBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


engine = create_engine(settings.sqlalchemy_database_url, future=True, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

Base = declarative_base(cls=DeclarativeBase)
