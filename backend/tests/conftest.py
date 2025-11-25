from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    test_db = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{test_db}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture()
async def client(db_session: Session) -> AsyncIterator[AsyncClient]:
    def _override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as c:
        yield c
    app.dependency_overrides.clear()
