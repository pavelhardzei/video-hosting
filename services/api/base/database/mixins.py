from base.database.config import SessionLocal


class SaveDeleteDBMixin:
    def save(self):
        with self.session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        with self.session() as session:
            session.delete(self)
            session.commit()

    @property
    def session(self):
        return SessionLocal
