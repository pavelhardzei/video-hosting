from unittest.mock import ANY

from auth.models import UserProfile
from fastapi import status
from testing.conftest import client


def test_signup(session):
    response = client.post('/api/v1/auth/signup/', json={'email': 'test@test.com',
                                                         'username': 'test',
                                                         'password': 'testing321'})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'id': ANY,
                               'email': 'test@test.com',
                               'username': 'test',
                               'is_active': True,
                               'role': UserProfile.RoleEnum.viewer}

    assert session.query(UserProfile).count() == 1
    user = session.query(UserProfile).first()
    assert user.check_password('testing321')
