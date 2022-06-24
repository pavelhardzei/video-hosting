from base.database.config import SessionLocal


class SaveDeleteDBMixin:
    def save(self):
        with SessionLocal() as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self):
        with SessionLocal() as session:
            session.delete(self)
            session.commit()
