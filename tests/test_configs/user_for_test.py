import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from BlogFastAPI.app.core.security import USER_AUTH


class AuthenticatedTestClient(TestClient):
    def __init__(self, application, user_token):
        super().__init__(application)
        self.user_token = user_token

    def request(self, *args, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {self.user_token}"
        return super().request(*args, headers=headers, **kwargs)

@pytest.fixture(scope="module")
def test_app():
    # Setup your FastAPI application for testing
    app = FastAPI()  # or however you create your FastAPI app
    return app

@pytest.fixture(scope="module")
def client():
    user_data = {
        "username": "test1@example.com",
        "password": "password"
    }
    # hashed_password = USER_AUTH.get_hash_password(user_data["password"])

    user_token = USER_AUTH.create_access_token(user_data)
    client = AuthenticatedTestClient(test_app, user_token)

    yield client