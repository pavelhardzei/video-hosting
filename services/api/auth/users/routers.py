from auth.dependencies import current_user
from auth.models import UserProfile
from auth.schemas import UserProfileSchema, UserProfileUpdateSchema
from base.database import crud
from fastapi import APIRouter, Depends, status

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
