from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from grpc_module.client import authorize

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/api/v1/auth/signin/')


def current_user_data(token: str = Depends(oauth2_scheme)) -> dict:
    data = authorize(token)

    return data
