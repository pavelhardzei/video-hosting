from datetime import datetime

from auth import permissions, utils
from auth.dependencies import current_user
from auth.models import UserProfile
from auth.schemas import schemas
from base.database import crud
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from fastapi import APIRouter, BackgroundTasks, Depends, status

router = APIRouter(
    prefix='/users/me',
    tags=['users']
)


@router.post('/send-email-confirmation/', response_model=schemas.DetailSchema)
def send_email_confirmation(background_tasks: BackgroundTasks, data: schemas.ConfirmationTokenBasedSchema,
                            user: UserProfile = Depends(current_user)):
    ''' Access token based confirmation email '''

    check_permissions(user, (permissions.UserEmailReady(), ))

    user.security.email_sent_time = datetime.utcnow()
    user.security.secondary_token = utils.create_token({'id': user.id})
    user.save()

    utils.send_mail([user.email], {'token': user.security.secondary_token, 'email_type': data.email_type.value},
                    data.email_type, background_tasks)

    return {'detail': 'Email sent'}


@router.get('/', response_model=schemas.UserProfileSchema,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': ErrorSchema}})
def get_user(user: UserProfile = Depends(current_user)):
    return user


@router.patch('/', response_model=schemas.UserProfileSchema)
def patch_user(data: schemas.UserProfileUpdateSchema, user: UserProfile = Depends(current_user)):
    crud.update(user, data)

    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(data: schemas.TokenSchema, user: UserProfile = Depends(current_user)):
    utils.decode_token(data.token)
    check_permissions(user, (permissions.UserSecondaryTokenValid(data.token), ))

    user.delete()

    return None
