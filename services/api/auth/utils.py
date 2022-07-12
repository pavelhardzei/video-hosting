from datetime import datetime, timedelta
from typing import Any, Dict, List

from auth.models import UserProfile
from base.settings import email_settings, settings
from fastapi import BackgroundTasks, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_access_token(token: str, **kwargs):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], **kwargs)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'{e}')
    return payload


fm = FastMail(ConnectionConfig(**email_settings.dict()))


def send_mail(recipients: List[str], body: Dict[str, Any], background_tasks: BackgroundTasks):
    message = MessageSchema(subject='Email Verification',
                            recipients=recipients,
                            template_body=body)

    background_tasks.add_task(fm.send_message, message, template_name='email/verification.html')


def get_user_by_id(user_id: int, session: Session):
    user = session.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is inactive')

    return user
