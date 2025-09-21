import pytest
from models import User

def test_user_model(test_db):
    # Test creating a user
    user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="hashedpass"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    assert user.id is not None
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"
    assert user.hashed_password == "hashedpass"

def test_user_model_unique_email(test_db):
    # Create first user
    user1 = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="hashedpass"
    )
    test_db.add(user1)
    test_db.commit()

    # Try to create another user with same email (should work at model level, constraint at DB level)
    user2 = User(
        first_name="Jane",
        last_name="Smith",
        email="john@example.com",  # Same email
        hashed_password="hashedpass2"
    )
    test_db.add(user2)

    # This should raise an IntegrityError due to unique constraint
    with pytest.raises(Exception):  # SQLAlchemy IntegrityError
        test_db.commit()
