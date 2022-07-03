from auth.models import UserProfile
from testing.conftest import client


def test_signup(session):
    assert session.query(UserProfile).count() == 0
