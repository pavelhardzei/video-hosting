from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from auth import exceptions
from auth.schemas.enums import ConfirmationTypeEnum
from base.settings import email_settings, settings
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_token(data: dict, expire_minutes: Optional[int] = None) -> str:
    access_token_expire_minutes = expire_minutes if expire_minutes else settings.access_token_expire_minutes

    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_token(token: str, **kwargs) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], **kwargs)
    except JWTError as e:
        raise exceptions.InvalidTokenException(detail=f'{e}')
    return payload


fm = FastMail(ConnectionConfig(**email_settings.dict()))


def send_mail(recipients: List[str], body: Dict[str, Any], email_type: ConfirmationTypeEnum,
              background_tasks: BackgroundTasks) -> None:
    message = MessageSchema(subject='Email Verification', recipients=recipients, template_body=body)

    background_tasks.add_task(fm.send_message, message, template_name=f'email/{email_type}.html')
