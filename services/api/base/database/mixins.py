from base.database.config import SessionLocal
from base.schemas.enums import ErrorCodeEnum
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class SaveDeleteDBMixin:
    _session_class = SessionLocal

    def save(self):
        with self.session_class() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'{e.orig}',
                                    headers={'Error-Code': ErrorCodeEnum.already_exists})

    def delete(self):
        with self.session_class() as session:
            session.delete(self)
            session.commit()

    @property
    def session_class(self):
        return self._session_class
