import pytest
from BlogFastAPI.tests.test_configs.user_for_test import client


@pytest.fixture(scope="module")
def test_user(client):
    user_test_data = {
        "email": "testuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    # Create user
    response = client.post("/register", json=user_test_data)
    assert response.status_code == 200

    return user_test_data
def test_login_url(test_user, client):
    email = test_user.get("email")
    password = test_user.get("email")

    login_data = {
        "username": email,
        "password": password
    }

    response = client.post("/token", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


