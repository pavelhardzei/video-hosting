from auth import utils
from auth.dependencies import current_user
from auth.models import UserProfile
from auth.schemas import DetailSchema, UserPasswordUpdateSchema, UserProfileSchema, UserProfileUpdateSchema
from base.database import crud
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


@router.put('/password/', response_model=DetailSchema)
def password(data: UserPasswordUpdateSchema, background_tasks: BackgroundTasks,
             user: UserProfile = Depends(current_user)):
    if not user.check_password(data.old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Old password is wrong')

    user.set_password(data.new_password)
    user.is_active = False
    user.save()

    utils.send_mail([user.email], {'token': utils.create_access_token({'id': user.id})},
                    'email/verification.html', background_tasks)

    return {'detail': 'Email sent'}
