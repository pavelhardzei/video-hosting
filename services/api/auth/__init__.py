from auth.models import UserProfile
from base.database.dependencies import session_dependency
from base.settings import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)):
    token_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not validate credentials',
                                    headers={'WWW-Authenticate': 'Bearer'})

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise token_exception

    user_id = payload.get('id')
    user = session.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user is None:
        raise token_exception

    return user
