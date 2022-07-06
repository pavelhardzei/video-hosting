from auth import current_user
from auth.models import UserProfile
from auth.schemas import TokenSchema, UserProfileCreateSchema, UserProfileSchema
from auth.utils import create_access_token
from base.database.dependencies import session_dependency
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

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


@router.post('/signin/', response_model=TokenSchema)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(session_dependency)):
    user = session.query(UserProfile).filter(UserProfile.email == form_data.username).first()

    if user is None or not user.check_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect email or password')
    access_token = create_access_token({'id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me/', response_model=UserProfileSchema)
def get_user(user: UserProfile = Depends(current_user)):
    return user
