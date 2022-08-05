from base.database.config import SessionLocal
from base.schemas.enums import ErrorCodeEnum
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session


class BaseDBMixin:
    _session_class = SessionLocal

    @property
    def session_class(self) -> scoped_session:
        return self._session_class


class SaveDBMixin(BaseDBMixin):
    def save(self) -> None:
        with self.session_class() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Unique constraints violation',
                                    headers={'Error-Code': ErrorCodeEnum.already_exists})


class DeleteDBMixin(BaseDBMixin):
    def delete(self) -> None:
        with self.session_class() as session:
            session.delete(self)
            session.commit()
