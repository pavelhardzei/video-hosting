from datetime import datetime, timedelta
from unittest.mock import ANY

from auth import utils
from auth.models import UserProfile
from auth.utils import fm
from base.settings import email_settings, settings
from fastapi import status
from freezegun import freeze_time
from testing import client


def test_signup_flow(session):
    fm.config.SUPPRESS_SEND = 1

    with fm.record_messages() as outbox:
        response = client.post('/api/v1/auth/signup/', json={'email': 'test@test.com',
                                                             'username': 'test',
                                                             'password': 'testing321'})
        assert len(outbox) == 1
        assert outbox[0]['from'] == email_settings.MAIL_FROM
        assert outbox[0]['to'] == 'test@test.com'

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'id': ANY,
                               'email': 'test@test.com',
                               'username': 'test',
                               'is_active': False,
                               'role': UserProfile.RoleEnum.viewer}

    assert session.query(UserProfile).count() == 1
    user = session.query(UserProfile).first()
    assert user.check_password('testing321')

    response = client.post('/api/v1/auth/email-verification/',
                           json={'id': user.id, 'token': utils.create_access_token({'id': user.id})})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'Email successfully verified'}

    session.refresh(user)
    assert user.is_active


def test_signup_email_already_exists(user):
    response = client.post('/api/v1/auth/signup/', json={'email': user.email,
                                                         'username': 'test',
                                                         'password': 'testing321'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail':
                               'duplicate key value violates unique constraint \"user_profile_email_key\"\n'
                               f'DETAIL:  Key (email)=({user.email}) already exists.\n'}


def test_email_verification_email_is_already_verified(user):
    response = client.post('/api/v1/auth/email-verification/',
                           json={'id': user.id, 'token': utils.create_access_token({'id': user.id})})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Email is already verified'}


def test_email_verification_resend(user1, user1_security):
    fm.config.SUPPRESS_SEND = 1

    with fm.record_messages() as outbox:
        response = client.post('/api/v1/auth/email-verification-resend/', json={'email': user1.email})

        assert len(outbox) == 1
        assert outbox[0]['from'] == email_settings.MAIL_FROM
        assert outbox[0]['to'] == user1.email

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'detail': 'Email sent'}

        response = client.post('/api/v1/auth/email-verification-resend/', json={'email': user1.email})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': f'You can resend email in {settings.email_resend_timeout_seconds} seconds'}

        with freeze_time(datetime.utcnow() + timedelta(seconds=settings.email_resend_timeout_seconds)):
            response = client.post('/api/v1/auth/email-verification-resend/', json={'email': user1.email})

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {'detail': 'Email sent'}

        assert len(outbox) == 2


def test_email_verification_resend_email_is_already_verified(user):
    response = client.post('/api/v1/auth/email-verification-resend/', json={'email': user.email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Email is already verified'}


def test_email_verification_resend_user_does_not_exist():
    response = client.post('/api/v1/auth/email-verification-resend/', json={'email': 'fake@example.com'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_signin(user, user_security):
    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'access_token': ANY, 'token_type': 'bearer'}


def test_signin_invalid_credentials(session, user):
    response = client.post('/api/v1/auth/signin/', data={'username': 'fake@fake.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}

    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'fake_password'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_signin_user_is_inactive(user1):
    response = client.post('/api/v1/auth/signin/', data={'username': user1.email,
                                                         'password': 'testing321'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive'}


def test_refresh_token(user, user_security, user_token):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token, 'token_type': 'bearer'})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'access_token': ANY, 'token_type': 'bearer'}

        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token, 'token_type': 'bearer'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Only the last generated token can be refreshed'}


def test_validate_refreshed_token(user, user_security, user_token):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token, 'token_type': 'bearer'})

        refreshed_token = response.json().get('access_token')
        response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {refreshed_token}'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'id': ANY,
                                   'email': user.email,
                                   'username': user.username,
                                   'is_active': True,
                                   'role': UserProfile.RoleEnum.viewer}


def test_refresh_token_invalid_token():
    response = client.post('/api/v1/auth/refresh-token/', json={'access_token': utils.create_access_token({'id': 0}),
                                                                'token_type': 'bearer'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token_user_is_inactive(user1_token):
    response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user1_token,
                                                                'token_type': 'bearer'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive'}


def test_get_current_user(user, user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': ANY,
                               'email': user.email,
                               'username': user.username,
                               'is_active': True,
                               'role': UserProfile.RoleEnum.viewer}


def test_get_current_user_inactive(user1_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user1_token}'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive'}


def test_get_current_user_invalid_token(user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}_fake'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature verification failed.'}

    response = client.get('/api/v1/auth/users/me/', headers={'Authorization':
                                                             f"Bearer {utils.create_access_token({'id': 0})}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_token_expired(user_token):
    with freeze_time(datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes, seconds=1)):
        response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature has expired.'}


def test_patch_current_user(user, user_token):
    response = client.patch('/api/v1/auth/users/me/',
                            json={'username': 'updated'},
                            headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': ANY,
                               'email': user.email,
                               'username': 'updated',
                               'is_active': True,
                               'role': UserProfile.RoleEnum.viewer}


def test_delete_current_user(user_token, session):
    response = client.delete('/api/v1/auth/users/me/',
                             headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() is None
    assert session.query(UserProfile).count() == 0
