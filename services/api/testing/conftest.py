import pytest
from auth import utils
from base.database.config import Base, engine
from base.database.dependencies import session_dependency
from base.database.mixins import SaveDeleteDBMixin
from base.main import app
from pytest_factoryboy import register
from sqlalchemy.orm import scoped_session, sessionmaker
from testing import test_session_dependency
from testing.auth.factories import UserProfileFactory

register(UserProfileFactory, 'user', email='test@test.com', username='test', is_active=True)


@pytest.fixture
def user_token(user):
    return utils.create_access_token({'id': user.id})


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def session(connection):
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))

    default_session_class = SaveDeleteDBMixin._session_class
    SaveDeleteDBMixin._session_class = session

    UserProfileFactory._meta.sqlalchemy_session = session

    app.dependency_overrides[session_dependency] = test_session_dependency(session)

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    yield session

    SaveDeleteDBMixin._session_class = default_session_class
    session.close()
    transaction.rollback()
