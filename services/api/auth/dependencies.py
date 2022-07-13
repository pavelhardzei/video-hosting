from auth import utils
from auth.models import UserProfile
from base.database.dependencies import session_dependency
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(token)

    user_id = payload.get('id')
    user = session.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is inactive')

    return user
