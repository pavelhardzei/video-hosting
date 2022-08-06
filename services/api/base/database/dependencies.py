from base.database.config import SessionLocal


def session_dependency():
    yield SessionLocal


def session_commit_hook():
    with SessionLocal() as session:
        yield

        session.commit()
