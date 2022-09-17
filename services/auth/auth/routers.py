from datetime import datetime

from auth import permissions, utils
from auth.models import UserProfile, UserRefreshTokens, UserSecurity
from auth.schemas import schemas
from auth.schemas.enums import ConfirmationTypeEnum
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/signup/', response_model=schemas.UserTokenSchema, status_code=status.HTTP_201_CREATED)
def signup(data: schemas.UserProfileCreateSchema, background_tasks: BackgroundTasks):
    user = UserProfile(**data.dict())
    user.set_password(data.password)

    user.security = UserSecurity()
    user.save()

    utils.send_mail([user.email], {'token': user.security.secondary_token,
                                   'email_type': ConfirmationTypeEnum.verification.value},
                    ConfirmationTypeEnum.verification, background_tasks)

    return {'access_token': None, 'refresh_token': None, 'user': user}


@router.post('/email-verification/', response_model=schemas.DetailSchema)
def email_verification(data: schemas.TokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (permissions.UserEmailNotVerified(), permissions.UserSecondaryTokenValid(data.token)))

    user.is_active = True
    user.security.secondary_token = None
    user.save()

    return {'detail': 'Email successfully verified'}


@router.put('/change-password/', response_model=schemas.DetailSchema)
def change_password(data: schemas.UserPasswordUpdateSchema, background_tasks: BackgroundTasks,
                    session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (permissions.UserActive(), permissions.UserSecondaryTokenValid(data.token)))

    user.set_password(data.new_password)
    user.security.secondary_token = None
    user.save()

    utils.send_mail([user.email], {'detail': 'password changed'},
                    ConfirmationTypeEnum.password_changed, background_tasks)

    return {'detail': 'Password changed'}


@router.post('/send-email-confirmation/', response_model=schemas.DetailSchema)
def send_email_confirmation(background_tasks: BackgroundTasks, data: schemas.ConfirmationEmailBasedSchema,
                            session: Session = Depends(session_dependency)):
    ''' Email address based confirmation email '''

    user = session.query(UserProfile).filter(UserProfile.email == data.email).first()

    if data.email_type == ConfirmationTypeEnum.verification:
        check_permissions(user, (permissions.UserEmailNotVerified(), ))
    else:
        check_permissions(user, (permissions.UserActive(), ))
    check_permissions(user, (permissions.UserEmailReady(), ))

    user.security.email_sent_time = datetime.utcnow()
    user.security.secondary_token = utils.create_token({'id': user.id})
    user.save()

    utils.send_mail([user.email], {'token': user.security.secondary_token, 'email_type': data.email_type.value},
                    data.email_type, background_tasks)

    return {'detail': 'Email sent'}


@router.post('/signin/', response_model=schemas.UserTokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == form_data.username).first()
    check_permissions(user, (permissions.UserCorrectCredentials(form_data.password), permissions.UserActive()))

    user.security.update_access_token()
    refresh_token = user.create_refresh_token()
    user.save()

    return {'access_token': user.security.access_token, 'refresh_token': refresh_token, 'user': user}


@router.post('/refresh-token/', response_model=schemas.AccessRefreshTokenSchema)
def refresh_token(data: schemas.RefreshTokenSchema, session: Session = Depends(session_dependency)):
    payload = utils.decode_token(data.refresh_token, options={'verify_exp': False})

    user = session.get(UserProfile, payload.get('user_id'))
    check_permissions(user, (permissions.UserActive(), permissions.UserRefreshTokenValid(data.refresh_token)))

    obj = session.get(UserRefreshTokens, payload.get('id'))
    obj.refresh_token = utils.create_token({'id': obj.id, 'user_id': user.id})

    user.security.update_access_token()
    user.save()

    return {'access_token': user.security.access_token, 'refresh_token': obj.refresh_token}
