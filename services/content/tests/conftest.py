import pytest
from base.database.config import Base, engine
from base.database.dependencies import session_commit_hook, session_dependency
from base.database.mixins import BaseDBMixin
from base.main import app
from sqlalchemy.orm import scoped_session, sessionmaker
from tests import test_session_dependency
from tests.content import factories as content_factories
from tests.users import factories as users_factories


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

    factories_attach_session(session)

    app.dependency_overrides[session_dependency] = test_session_dependency(session)
    app.dependency_overrides[session_commit_hook] = lambda: None

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    yield session

    BaseDBMixin._session_class = default_session_class
    session.close()
    transaction.rollback()


def factories_attach_session(session):
    content_factories.MediaFactory._meta.sqlalchemy_session = session
    content_factories.ContentFactory._meta.sqlalchemy_session = session
    content_factories.MovieFactory._meta.sqlalchemy_session = session
    content_factories.SerialFactory._meta.sqlalchemy_session = session
    content_factories.SeasonFactory._meta.sqlalchemy_session = session
    content_factories.EpisodeFactory._meta.sqlalchemy_session = session
    content_factories.CountryFactory._meta.sqlalchemy_session = session
    content_factories.GenreFactory._meta.sqlalchemy_session = session
    content_factories.ActorFactory._meta.sqlalchemy_session = session
    content_factories.DirectorFactory._meta.sqlalchemy_session = session
    content_factories.ContentCountriesFactory._meta.sqlalchemy_session = session
    content_factories.ContentGenresFactory._meta.sqlalchemy_session = session
    content_factories.ContentActorsFactory._meta.sqlalchemy_session = session
    content_factories.ContentDirectorsFactory._meta.sqlalchemy_session = session

    users_factories.UserLibraryFactory._meta.sqlalchemy_session = session
