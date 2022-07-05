from auth.models import UserProfile
from base.database.dependencies import session_dependency
from base.settings import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload['id']

    user = session.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials',
                            headers={'WWW-Authenticate': 'Bearer'})

    return user
