from fastapi.testclient import TestClient
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.auth.user_manager.user_auth import (
    USER_AUTH,
    UserAuth,
    oauth2_scheme
)
from .config import client
import pytest

@pytest.fixture(scope="module")
def test_user():
    user_test_data = {
        "email": "testuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    # Create user
    response = client.post("/register", json=user_test_data)
    print(response)
    assert response.status_code == 200

    return user_test_data
def test_login_url(test_user):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


