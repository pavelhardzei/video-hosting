from base.database.config import SessionLocal


def session_dependency():
    with SessionLocal() as session:
        yield session
