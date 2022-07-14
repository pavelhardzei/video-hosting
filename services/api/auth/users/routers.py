from datetime import datetime

from auth import utils
from auth.dependencies import current_user
from auth.models import UserProfile
from auth.permissions import UserEmailReady
from auth.schemas import DetailSchema, UserPasswordUpdateSchema, UserProfileSchema, UserProfileUpdateSchema
from base.database import crud
from base.permissions import check_permissions
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

router = APIRouter(
    prefix='/users/me'
)


@router.get('/', response_model=UserProfileSchema)
def get_user(user: UserProfile = Depends(current_user)):
    return user


@router.patch('/', response_model=UserProfileSchema)
def patch_user(data: UserProfileUpdateSchema, user: UserProfile = Depends(current_user)):
    crud.update(user, data)

    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: UserProfile = Depends(current_user)):
    user.delete()

    return None


@router.post('/change-password-request/', response_model=DetailSchema)
def change_password_request(background_tasks: BackgroundTasks, user: UserProfile = Depends(current_user)):
    check_permissions(user, (UserEmailReady(), ))

    user.security.email_sent_time = datetime.utcnow()
    user.security.password_token = utils.create_access_token({'id': user.id})
    user.save()

    utils.send_mail([user.email], {'token': user.security.password_token},
                    'email/password_change.html', background_tasks)

    return {'detail': 'Follow the changing password link on the email'}


@router.put('/change-password/', response_model=DetailSchema)
def change_password(data: UserPasswordUpdateSchema, background_tasks: BackgroundTasks,
                    user: UserProfile = Depends(current_user)):
    if not user.security.check_password_token(data.password_token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token is invalid')
    utils.decode_access_token(data.password_token)

    user.set_password(data.new_password)
    user.security.password_token = None
    user.save()

    utils.send_mail([user.email], {'token': user.security.token},
                    'email/password_changed.html', background_tasks)

    return {'detail': 'Password changed'}
