from datetime import datetime, timedelta
from unittest.mock import ANY

from auth import utils
from auth.models import UserProfile
from auth.schemas.enums import ConfirmationTypeEnum, RoleEnum
from auth.utils import fm
from base.schemas.enums import ErrorCodeEnum
from base.settings import email_settings, settings
from fastapi import status
from freezegun import freeze_time
from tests import client


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
    assert response.json() == {'access_token': None,
                               'user': {'id': ANY,
                                        'email': 'test@test.com',
                                        'username': 'test',
                                        'is_active': False,
                                        'role': RoleEnum.viewer}}

    assert session.query(UserProfile).count() == 1
    user = session.query(UserProfile).first()
    assert user.check_password('testing321')

    response = client.post('/api/v1/auth/email-verification/', json={'token': user.security.secondary_token})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'Email successfully verified'}

    session.refresh(user)
    assert user.is_active
    assert user.security.secondary_token is None


def test_signup_email_already_exists(user):
    response = client.post('/api/v1/auth/signup/', json={'email': user.email,
                                                         'username': 'test',
                                                         'password': 'testing321'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Unique constraints violation', 'error_code': ErrorCodeEnum.already_exists}


def test_email_verification_email_is_already_verified(user, user_security):
    response = client.post('/api/v1/auth/email-verification/', json={'token': user.security.secondary_token})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Email is already verified', 'error_code': ErrorCodeEnum.already_verified}


def test_email_verification_invalid_token(user1, user1_security):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/email-verification/',
                               json={'token': utils.create_token({'id': user1.id})})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}


def test_email_confirmation(user1, user1_security):
    fm.config.SUPPRESS_SEND = 1

    with fm.record_messages() as outbox:
        response = client.post('/api/v1/auth/email-confirmation/',
                               json={'email': user1.email, 'email_type': ConfirmationTypeEnum.verification})

        assert len(outbox) == 1
        assert outbox[0]['from'] == email_settings.MAIL_FROM
        assert outbox[0]['to'] == user1.email

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'detail': 'Email sent'}

        user1.is_active = True
        user1.save()

        response = client.post('/api/v1/auth/email-confirmation/',
                               json={'email': user1.email, 'email_type': ConfirmationTypeEnum.password_change})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': f'You can resend email in {settings.email_resend_timeout_seconds} seconds',
                                   'error_code': ErrorCodeEnum.timeout_error}

        with freeze_time(datetime.utcnow() + timedelta(seconds=settings.email_resend_timeout_seconds)):
            response = client.post('/api/v1/auth/email-confirmation/',
                                   json={'email': user1.email, 'email_type': ConfirmationTypeEnum.password_change})

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {'detail': 'Email sent'}

        assert len(outbox) == 2


def test_email_confirmation_email_is_already_verified(user):
    response = client.post('/api/v1/auth/email-confirmation/',
                           json={'email': user.email, 'email_type': ConfirmationTypeEnum.verification})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Email is already verified', 'error_code': ErrorCodeEnum.already_verified}


def test_email_confirmation_user_does_not_exist():
    response = client.post('/api/v1/auth/email-confirmation/',
                           json={'email': 'fake@example.com', 'email_type': ConfirmationTypeEnum.verification})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found', 'error_code': ErrorCodeEnum.not_found}


def test_signin(user, user_security):
    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'access_token': user.security.access_token,
                               'user': {'id': user.id,
                                        'email': user.email,
                                        'username': user.username,
                                        'is_active': user.is_active,
                                        'role': user.role}}


def test_signin_invalid_credentials(session, user):
    response = client.post('/api/v1/auth/signin/', data={'username': 'fake@fake.com',
                                                         'password': 'testing321'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password', 'error_code': ErrorCodeEnum.invalid_credentials}

    response = client.post('/api/v1/auth/signin/', data={'username': 'test@test.com',
                                                         'password': 'fake_password'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password', 'error_code': ErrorCodeEnum.invalid_credentials}


def test_signin_user_is_inactive(user1):
    response = client.post('/api/v1/auth/signin/', data={'username': user1.email,
                                                         'password': 'testing321'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive', 'error_code': ErrorCodeEnum.user_inactive}


def test_refresh_token(user, user_security, user_token):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'access_token': user.security.access_token}
        assert user.security.access_token != user_token

        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}


def test_refresh_expired_token(user, user_security, user_token):
    with freeze_time(datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes, seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'access_token': user.security.access_token}
        assert user.security.access_token != user_token


def test_validate_refreshed_token(user, user_security, user_token):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user_token})
        response = client.get('/api/v1/auth/users/me/',
                              headers={'Authorization': f'Bearer {user.security.access_token}'})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'id': ANY,
                                   'email': user.email,
                                   'username': user.username,
                                   'is_active': True,
                                   'role': RoleEnum.viewer}


def test_refresh_token_invalid_token(user, user_security):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.post('/api/v1/auth/refresh-token/',
                               json={'access_token': utils.create_token({'id': user.id})})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}


def test_refresh_token_user_is_inactive(user1_token):
    response = client.post('/api/v1/auth/refresh-token/', json={'access_token': user1_token})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive', 'error_code': ErrorCodeEnum.user_inactive}


def test_get_current_user(user, user_security, user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': ANY,
                               'email': user.email,
                               'username': user.username,
                               'is_active': True,
                               'role': RoleEnum.viewer}


def test_get_current_user_not_authenticated():
    response = client.get('/api/v1/auth/users/me/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated', 'error_code': ErrorCodeEnum.base_error}


def test_get_current_user_inactive(user1_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user1_token}'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'User is inactive', 'error_code': ErrorCodeEnum.user_inactive}


def test_get_current_user_invalid_token(user, user_security, user_token):
    response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}_fake'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature verification failed.', 'error_code': ErrorCodeEnum.invalid_token}

    response = client.get('/api/v1/auth/users/me/', headers={'Authorization':
                                                             f"Bearer {utils.create_token({'id': 0})}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found', 'error_code': ErrorCodeEnum.not_found}

    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        invalid_token = utils.create_token({'id': user.id})

        response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f"Bearer {invalid_token}"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}


def test_get_current_user_token_expired(user_token):
    with freeze_time(datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes, seconds=1)):
        response = client.get('/api/v1/auth/users/me/', headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Signature has expired.', 'error_code': ErrorCodeEnum.invalid_token}


def test_patch_current_user(user, user_security, user_token):
    response = client.patch('/api/v1/auth/users/me/',
                            json={'username': 'updated'},
                            headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': ANY,
                               'email': user.email,
                               'username': 'updated',
                               'is_active': True,
                               'role': RoleEnum.viewer}


def test_delete_current_user_flow(user, user_token, user_security, session):
    fm.config.SUPPRESS_SEND = 1

    with fm.record_messages() as outbox:
        response = client.post('/api/v1/auth/users/me/email-confirmation/',
                               json={'email_type': ConfirmationTypeEnum.account_deletion},
                               headers={'Authorization': f'Bearer {user_token}'})

        assert len(outbox) == 1
        assert outbox[0]['from'] == email_settings.MAIL_FROM
        assert outbox[0]['to'] == user.email

    response = client.delete('/api/v1/auth/users/me/',
                             json={'token': user.security.secondary_token},
                             headers={'Authorization': f'Bearer {user_token}'})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.json() is None
    assert session.query(UserProfile).count() == 0


def test_delete_current_user_invalid_token(user, user_token, user_security):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.delete('/api/v1/auth/users/me/',
                                 json={'token': utils.create_token({'id': user.id})},
                                 headers={'Authorization': f'Bearer {user_token}'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}


def test_user_password_change_flow(user, user_security, session):
    fm.config.SUPPRESS_SEND = 1

    with fm.record_messages() as outbox:
        response = client.post('/api/v1/auth/email-confirmation/',
                               json={'email': user.email, 'email_type': ConfirmationTypeEnum.password_change})

        assert len(outbox) == 1
        assert outbox[0]['from'] == email_settings.MAIL_FROM
        assert outbox[0]['to'] == user.email

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'detail': 'Email sent'}

        response = client.put('/api/v1/auth/change-password/',
                              json={'new_password': 'updated_password', 'token': user.security.secondary_token})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'detail': 'Password changed'}

        session.refresh(user)
        assert user.check_password('updated_password')
        assert user.security.secondary_token is None
        assert len(outbox) == 2


def test_user_password_change_invalid_token(user, user_security):
    with freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        response = client.put('/api/v1/auth/change-password/',
                              json={'new_password': 'updated_password',
                                    'token': f"{utils.create_token({'id': user.id})}"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Token is invalid or expired', 'error_code': ErrorCodeEnum.invalid_token}
