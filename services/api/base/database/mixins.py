from base.database.config import SessionLocal


class SaveDeleteDBMixin:
    def save(self):
        with SessionLocal() as session:
            session.add(self)
            session.commit()

    def delete(self):
        with SessionLocal() as session:
            session.delete(self)
            session.commit()
