import pytest
from utils.auth import create_user, get_user_by_email, verify_password, pwd_context
from schemas import UserCreate

def test_password_hashing():
    password = "testpassword"
    hashed = pwd_context.hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_user(test_db):
    user_data = UserCreate(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        password="password123"
    )
    user = create_user(test_db, user_data)
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.email == "jane@example.com"
    assert user.hashed_password != "password123"  # Should be hashed
    assert pwd_context.verify("password123", user.hashed_password)

def test_get_user_by_email(test_db):
    # First create a user
    user_data = UserCreate(
        first_name="Bob",
        last_name="Wilson",
        email="bob@example.com",
        password="password123"
    )
    create_user(test_db, user_data)

    # Test retrieval
    user = get_user_by_email(test_db, "bob@example.com")
    assert user is not None
    assert user.first_name == "Bob"
    assert user.email == "bob@example.com"

    # Test non-existent user
    user = get_user_by_email(test_db, "nonexistent@example.com")
    assert user is None

def test_verify_password():
    password = "mypassword"
    hashed = pwd_context.hash(password)

    # Correct password
    assert verify_password(password, hashed)

    # Wrong password
    assert not verify_password("wrongpassword", hashed)

    # Empty password
    assert not verify_password("", hashed)
