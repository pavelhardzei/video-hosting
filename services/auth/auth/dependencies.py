from auth import utils
from auth.database.models import UserProfile
from auth.permissions import UserAccessTokenValid, UserActive
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)) -> UserProfile:
    payload = utils.decode_access_token(token)

    user = session.get(UserProfile, payload.get('id'))
    check_permissions(user, (UserActive(), UserAccessTokenValid(token)))

    return user
