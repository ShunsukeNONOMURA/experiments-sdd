from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base class shared across models."""


def get_db() -> Generator:
    """Yield a SQLAlchemy session scoped to the request lifecycle."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
