from auth import utils
from auth.models import UserProfile
from auth.schemas import TokenSchema, UserProfileCreateSchema, UserProfileSchema
from auth.users.routers import router as users_router
from base.database.dependencies import session_dependency
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

router.include_router(users_router)


@router.post('/signup/', response_model=UserProfileSchema, status_code=status.HTTP_201_CREATED)
def signup(data: UserProfileCreateSchema):
    user = UserProfile(**data.dict())
    user.set_password(data.password)

    # TODO: implement email verification
    user.is_active = True
    user.save()

    return user


@router.post('/signin/', response_model=TokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == form_data.username).first()

    if user is None or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password')
    access_token = utils.create_access_token({'id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
