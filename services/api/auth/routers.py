from auth.models import UserProfile
from auth.schemas import UserProfileCreateSchema, UserProfileSchema
from fastapi import APIRouter, status

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/signup/', response_model=UserProfileSchema, status_code=status.HTTP_201_CREATED)
def signup(user: UserProfileCreateSchema):
    user_model = UserProfile(**user.dict())
    user_model.set_password(user.password)

    # TODO: implement email verification
    user_model.is_active = True
    user_model.save()

    return user_model
