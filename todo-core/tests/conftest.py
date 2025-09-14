"""Test configuration and fixtures for todo-core."""

import os
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from todo_core.models import Base

@pytest.fixture(scope="session")
def db_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a temporary database file."""
    db_dir = tmp_path_factory.mktemp("data")
    return db_dir / "test.db"

@pytest.fixture(scope="session")
def engine(db_path: Path) -> Generator[Engine, None, None]:
    """Create a SQLite database engine for testing."""
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        if db_path.exists():
            os.unlink(db_path)

@pytest.fixture
def db_session(engine: Engine) -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()