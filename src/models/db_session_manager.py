from contextlib import contextmanager

from src.models.db_engine import SessionLocal


class DBSessionManager:
    @contextmanager
    def session(self):
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
