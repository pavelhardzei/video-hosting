from datetime import datetime, timedelta
from unittest.mock import ANY

from auth.models import UserProfile
from auth.utils import create_access_token
from base.settings import settings
from fastapi import status
from freezegun import freeze_time
from testing import client


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


def test_signin(user):
    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'access_token': ANY, 'token_type': 'bearer'}


def test_signin_invalid_credentials(session, user):
    response = client.post('/api/v1/auth/signin/', data={'username': 'fake@fake.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'fake_password'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': ANY,
                               'email': 'test@test.com',
                               'username': 'test',
                               'is_active': True,
                               'role': UserProfile.RoleEnum.viewer}


def test_get_current_user_invalid_token(user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}_fake'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature verification failed.'}

    response = client.get('/api/v1/auth/users/me/', headers={'Authorization':
                                                             f"Bearer {create_access_token({'id': 0})}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_token_expired(user_token):
    with freeze_time(datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes, seconds=1)):
        response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature has expired.'}
