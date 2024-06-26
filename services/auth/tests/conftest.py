from unittest.mock import patch

import pytest
from base.database.config import Base, engine
from base.database.dependencies import session_commit_hook, session_dependency
from base.database.mixins import BaseDBMixin
from base.main import app
from sqlalchemy.orm import scoped_session, sessionmaker
from tests import test_session_dependency
from tests.auth.factories import UserProfileFactory, UserRefreshTokensFactory, UserSecurityFactory


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def session(connection):
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))

    default_session_class = BaseDBMixin._session_class
    BaseDBMixin._session_class = session

    UserProfileFactory._meta.sqlalchemy_session = session
    UserSecurityFactory._meta.sqlalchemy_session = session
    UserRefreshTokensFactory._meta.sqlalchemy_session = session

    app.dependency_overrides[session_dependency] = test_session_dependency(session)
    app.dependency_overrides[session_commit_hook] = lambda: None

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    with patch('grpc_module.service.SessionLocal', session):
        yield session

    BaseDBMixin._session_class = default_session_class
    session.close()
    transaction.rollback()
