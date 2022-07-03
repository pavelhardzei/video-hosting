import pytest
from base.database.config import Base, engine
from base.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session, sessionmaker
from testing.auth.factories import UserProfileFactory

client = TestClient(app)


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture()
def session(connection):
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))

    UserProfileFactory._meta.sqlalchemy_session = session

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    yield session

    session.close()
    transaction.rollback()
