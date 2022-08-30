from base import exceptions
from base.database.config import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session


class BaseDBMixin:
    _session_class = SessionLocal

    @property
    def session_class(self) -> scoped_session:
        return self._session_class


class SaveDBMixin(BaseDBMixin):
    def save(self) -> None:
        try:
            self.session_class.add(self)
            self.session_class.flush()
        except IntegrityError:
            raise exceptions.AlreadyExistsException()


class DeleteDBMixin(BaseDBMixin):
    def delete(self) -> None:
        self.session_class.delete(self)
        self.session_class.flush()
