from auth import utils
from auth.models import UserProfile
from auth.permissions import UserActive
from base.database.dependencies import session_dependency
from base.permissions import check_permissions
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/signin/')


def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(session_dependency)):
    payload = utils.decode_access_token(token)

    user_id = payload.get('id')
    user = session.query(UserProfile).filter(UserProfile.id == user_id).first()

    check_permissions(user, (UserActive, ))

    if not user.security.check_token(token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token is invalid or expired')

    return user
