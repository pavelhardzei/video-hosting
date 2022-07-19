from base.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_session_dependency(session):
    def session_dependency():
        yield session

    return session_dependency
