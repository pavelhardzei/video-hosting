from datetime import datetime, timedelta

from base.settings import settings
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

# for plain password encryption
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict):
    '''For access token creating'''

    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_access_token(token: str):
    '''For access token decoding'''

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'{e}')
    return payload
