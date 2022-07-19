from base.database.config import SessionLocal


class SaveDeleteDBMixin:
    _session_class = SessionLocal

    def save(self):
        with self.session_class() as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        with self.session_class() as session:
            session.delete(self)
            session.commit()

    @property
    def session_class(self):
        return self._session_class
