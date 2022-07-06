from auth.dependencies import current_user
from auth.models import UserProfile
from auth.schemas import UserProfileSchema, UserProfileUpdateSchema
from base.database import crud
from fastapi import APIRouter, Depends

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
