from datetime import datetime

from auth import utils
from auth.models import UserProfile, UserSecurity
from auth.permissions import UserActive, UserEmailNotVerified, UserEmailReady, UserTokenValid
from auth.schemas import DetailSchema, EmailSchema, TokenSchema, UserProfileCreateSchema, UserProfileSchema
from auth.users.routers import router as users_router
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
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

    utils.send_mail([user.email], {'token': user.security.token},
                    'email/verification.html', background_tasks)

    return user


@router.post('/email-verification/', response_model=DetailSchema)
def email_verification(data: TokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(data.access_token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (UserEmailNotVerified(), UserTokenValid(data.access_token)))

    user.is_active = True
    user.save()

    return {'detail': 'Email successfully verified'}


@router.post('/email-verification-resend/', response_model=DetailSchema)
def email_verification_resend(background_tasks: BackgroundTasks, data: EmailSchema,
                              session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == data.email).first()
    check_permissions(user, (UserEmailNotVerified(), UserEmailReady()))

    user.security.email_sent_time = datetime.utcnow()
    user.security.token = utils.create_access_token({'id': user.id})
    user.save()

    utils.send_mail([user.email], {'token': user.security.token},
                    'email/verification.html', background_tasks)

    return {'detail': 'Email sent'}


@router.post('/signin/', response_model=TokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == form_data.username).first()

    if user is None or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password')

    check_permissions(user, (UserActive(), ))

    user.security.token = utils.create_access_token({'id': user.id})
    user.save()

    return {'access_token': user.security.token}


@router.post('/refresh-token/', response_model=TokenSchema)
def refresh_token(data: TokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(data.access_token, options={'verify_exp': False})

    user = session.query(UserProfile).filter(UserProfile.id == payload.get('id')).first()
    check_permissions(user, (UserActive(), UserTokenValid(data.access_token)))

    user.security.token = utils.create_access_token({'id': user.id})
    user.save()

    return {'access_token': user.security.token}
