from base.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session

client = TestClient(app)


def test_session_dependency(session: scoped_session):
    def session_dependency():
        yield session

    return session_dependency
