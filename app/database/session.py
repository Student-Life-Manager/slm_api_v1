from typing import Generator

from sqlalchemy.orm import Session

from app.database.engine import session as SessionLocal


def get_db() -> Generator:
    """
    Get the database session.

    Yields:
        Generator: The database session.
    """
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()
