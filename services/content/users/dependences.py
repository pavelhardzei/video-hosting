from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from grpc_module.client import authorize

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/api/v1/auth/signin/')


def current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    id = authorize(token)

    return id
