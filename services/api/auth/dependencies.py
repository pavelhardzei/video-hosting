from auth import utils
from base.database.dependencies import session_dependency
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(token)

    user_id = payload.get('id')
    user = utils.get_user_by_id(user_id, session)

    return user
