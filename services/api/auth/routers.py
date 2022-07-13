from datetime import datetime

from auth import utils
from auth.models import UserProfile, UserSecurity
from auth.schemas import (DetailSchema, EmailSchema, EmailVerificationSchema, TokenSchema, UserProfileCreateSchema,
                          UserProfileSchema)
from auth.users.routers import router as users_router
from base.database.dependencies import session_dependency
from base.settings import settings
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, selectinload

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

    utils.send_mail([user.email], {'id': user.id, 'token': utils.create_access_token({'id': user.id})},
                    background_tasks)

    return user


@router.post('/email-verification/', response_model=DetailSchema)
def email_verification(data: EmailVerificationSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(data.token)

    if data.id != payload.get('id'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email verification failed')

    user = session.get(UserProfile, data.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email is already verified')

    user.is_active = True
    user.save()

    return {'detail': 'Email successfully verified'}


@router.post('/email-verification-resend/', response_model=DetailSchema)
def email_verification_resend(background_tasks: BackgroundTasks, data: EmailSchema,
                              session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).options(selectinload(UserProfile.security))\
                                     .filter(UserProfile.email == data.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    if user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email is already verified')

    if not (user.security.email_sent_time is None or user.security.is_resend_ready):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'You can resend email in {settings.email_resend_timeout_seconds} seconds')

    utils.send_mail([user.email], {'id': user.id, 'token': utils.create_access_token({'id': user.id})},
                    background_tasks)

    user.security.email_sent_time = datetime.utcnow()
    user.security.save()

    return {'detail': 'Email sent'}


@router.post('/signin/', response_model=TokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).options(selectinload(UserProfile.security))\
                                     .filter(UserProfile.email == form_data.username).first()

    if user is None or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is inactive')

    access_token = utils.create_access_token({'id': user.id})

    user.security.token = access_token
    user.security.save()

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh-token/', response_model=TokenSchema)
def refresh_token(data: TokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(data.access_token, options={'verify_exp': False})

    user_id = payload.get('id')
    user = session.query(UserProfile).options(selectinload(UserProfile.security))\
                                     .filter(UserProfile.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is inactive')

    if user.security.token != data.access_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only the last generated token can be refreshed')

    token = utils.create_access_token({'id': user_id})
    user.security.token = token
    user.security.save()

    return {'access_token': token, 'token_type': 'bearer'}
