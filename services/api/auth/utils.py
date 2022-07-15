from datetime import datetime, timedelta
from typing import Any, Dict, List

from auth.schemas.enums import EmailTypeEnum
from base.settings import email_settings, settings
from fastapi import BackgroundTasks, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict, expire_minutes=None):
    access_token_expire_minutes = expire_minutes if expire_minutes else settings.access_token_expire_minutes

    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)})
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
email_templates = {EmailTypeEnum.verification: 'email/verification.html',
                   EmailTypeEnum.password_change: 'email/password_change.html',
                   EmailTypeEnum.password_changed: 'email/password_changed.html'}


def send_mail(recipients: List[str], body: Dict[str, Any],
              email_type: EmailTypeEnum, background_tasks: BackgroundTasks):
    message = MessageSchema(subject='Email Verification',
                            recipients=recipients,
                            template_body=body)

    background_tasks.add_task(fm.send_message, message, template_name=email_templates[email_type])
