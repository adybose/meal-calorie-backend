import pytest
from fastapi import HTTPException

def test_register_user(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com",
        "password": "password123"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client):
    user_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com",
        "password": "password123"
    }

    # Register first time
    client.post("/auth/register", json=user_data)

    # Try to register again
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(client):
    # First register
    user_data = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com",
        "password": "password123"
    }
    client.post("/auth/register", json=user_data)

    # Then login
    login_data = {
        "email": "charlie@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert "user" in data
    assert data["user"]["email"] == "charlie@example.com"

def test_login_wrong_password(client):
    # First register
    user_data = {
        "first_name": "David",
        "last_name": "Miller",
        "email": "david@example.com",
        "password": "password123"
    }
    client.post("/auth/register", json=user_data)

    # Try login with wrong password
    login_data = {
        "email": "david@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_nonexistent_user(client):
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_register_invalid_data(client):
    # Test missing required fields
    user_data = {
        "first_name": "Test",
        "email": "test@example.com"
        # Missing last_name and password
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422  # Validation error

def test_login_invalid_data(client):
    # Test missing password
    login_data = {
        "email": "test@example.com"
        # Missing password
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 422  # Validation error
