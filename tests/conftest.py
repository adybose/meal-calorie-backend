import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db

# Set test environment variables
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def test_db(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        # Clear all tables before each test
        from database import Base
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    # Mock user for authentication
    from models import User
    mock_user = User(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        hashed_password="hashed"
    )

    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    from auth import get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c
