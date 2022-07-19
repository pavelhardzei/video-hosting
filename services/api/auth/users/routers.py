from auth import utils
from auth.dependencies import current_user
from auth.models import UserProfile
from auth.permissions import UserSecondaryTokenValid
from auth.schemas.schemas import TokenSchema, UserProfileSchema, UserProfileUpdateSchema
from base.database import crud
from base.permissions import check_permissions
from base.schemas.schemas import ErrorSchema
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix='/users/me'
)


@router.get('/', response_model=UserProfileSchema, responses={status.HTTP_401_UNAUTHORIZED: {'model': ErrorSchema}})
def get_user(user: UserProfile = Depends(current_user)):
    return user


@router.patch('/', response_model=UserProfileSchema)
def patch_user(data: UserProfileUpdateSchema, user: UserProfile = Depends(current_user)):
    crud.update(user, data)

    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(data: TokenSchema, user: UserProfile = Depends(current_user)):
    utils.decode_token(data.token)
    check_permissions(user, (UserSecondaryTokenValid(data.token), ))

    user.delete()

    return None
