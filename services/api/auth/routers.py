from datetime import datetime

from auth import utils
from auth.models import UserProfile, UserSecurity
from auth.permissions import (UserAccessTokenValid, UserActive, UserEmailNotVerified, UserEmailReady,
                              UserSecondaryTokenValid)
from auth.schemas.enums import EmailTypeEnum
from auth.schemas.schemas import (AccessTokenSchema, DetailSchema, EmailSchema, TokenSchema, UserPasswordUpdateSchema,
                                  UserProfileCreateSchema, UserProfileSchema)
from auth.users.routers import router as users_router
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from base.schemas.enums import ErrorCodeEnum
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

router.include_router(users_router)


@router.post('/signup/', response_model=UserProfileSchema, status_code=status.HTTP_201_CREATED)
def signup(data: UserProfileCreateSchema, background_tasks: BackgroundTasks):
    user = UserProfile(**data.dict())
    user.set_password(data.password)

    user.security = UserSecurity()
    user.save()

    utils.send_mail([user.email], {'token': user.security.secondary_token},
                    EmailTypeEnum.verification, background_tasks)

    return user


@router.post('/email-verification/', response_model=DetailSchema)
def email_verification(data: TokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (UserEmailNotVerified(), UserSecondaryTokenValid(data.token)))

    user.is_active = True
    user.security.secondary_token = None
    user.save()

    return {'detail': 'Email successfully verified'}


@router.put('/change-password/', response_model=DetailSchema)
def change_password(data: UserPasswordUpdateSchema, background_tasks: BackgroundTasks,
                    session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (UserActive(), UserSecondaryTokenValid(data.token)))

    user.set_password(data.new_password)
    user.security.secondary_token = None
    user.save()

    utils.send_mail([user.email], {'detal': 'password changed'},
                    EmailTypeEnum.password_changed, background_tasks)

    return {'detail': 'Password changed'}


@router.post('/email-confirmation/', response_model=DetailSchema)
def email_confirmation(background_tasks: BackgroundTasks, data: EmailSchema,
                       session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == data.email).first()

    if data.email_type == EmailTypeEnum.verification:
        check_permissions(user, (UserEmailNotVerified(), ))
    check_permissions(user, (UserEmailReady(), ))

    user.security.email_sent_time = datetime.utcnow()
    user.security.secondary_token = utils.create_token({'id': user.id})
    user.save()

    utils.send_mail([user.email], {'token': user.security.secondary_token},
                    data.email_type, background_tasks)

    return {'detail': 'Email sent'}


@router.post('/signin/', response_model=AccessTokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == form_data.username).first()

    if user is None or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password',
                            headers={'Error-Code': ErrorCodeEnum.invalid_credentials})

    check_permissions(user, (UserActive(), ))

    user.security.access_token = utils.create_token({'id': user.id})
    user.save()

    return {'access_token': user.security.access_token}


@router.post('/refresh-token/', response_model=AccessTokenSchema)
def refresh_token(data: AccessTokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.access_token, options={'verify_exp': False})

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (UserActive(), UserAccessTokenValid(data.access_token)))

    user.security.access_token = utils.create_token({'id': user.id})
    user.save()

    return {'access_token': user.security.access_token}
