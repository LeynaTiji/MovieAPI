import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app, get_db
from app.database import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

#separate db connection

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# override it with test database so API requests tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def setup_database():
    # creates tables before test runs
    Base.metadata.create_all(bind=engine)
    yield
    # deletes tables after tests
    Base.metadata.drop_all(bind=engine)

