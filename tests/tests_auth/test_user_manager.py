from .config import client
from BlogFastAPI.app.auth.user_manager import user_auth
from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.db.models.models import User
from datetime import timedelta
import pytest

USER_DATA = {
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "password123"
}

@pytest.fixture
def user_manager():
    oauth_scheme = user_auth.oauth2_scheme
    user_auth_manager = user_auth.UserAuth(oauth_scheme)
    return user_auth_manager

def test_hash_password(user_manager):
    """
        Test responsible for check properhash of my password
    :return:
    """
    plain_password = "password123"
    hashed_password = user_manager.get_hash_password(plain_password)

    assert plain_password != hashed_password


def test_verify_password(user_manager):
    """
        Test responsible for verify of my password
    :return:
    """
    plain_password = "password123"
    hashed_password = user_manager.get_hash_password(plain_password)

    correct_password = user_manager.verify_password(
        plain_password, hashed_password
    )

    assert correct_password


def test_access_token_creation(user_manager):
    user_data = {"email": "test@test.pl"}
    expires_delta = timedelta(minutes=30)

    # Generate token
    token = user_manager.create_access_token(user_data, expires_delta)

    # Decode token
    decoded_token = user_manager.decode_access_token(token)

    assert decoded_token["email"] == user_data["email"]


def test_get_user(user_manager):
    with SessionLocal() as db_test_connection:
        user_test_db = User(**USER_DATA)
        user_test_db.hashed_password = user_manager.get_hash_password(
            USER_DATA["password"]
        )

        db_test_connection.add(user_test_db)
        db_test_connection.commit()

        db_found_user = user_manager.get_user(
            user_test_db.email,
            db_test_connection
        )

        assert db_found_user is not None
        assert db_found_user.email == USER_DATA["email"]

def test_authenticate_user(user_manager):
    with SessionLocal() as db_test_connection:
        user_test_db = User(**USER_DATA)
        user_test_db_password = USER_DATA["password"]
        user_test_db.hashed_password = user_manager.get_hash_password(
            USER_DATA["password"]
        )

        db_test_connection.add(user_test_db)
        db_test_connection.commit()

        db_found_user = user_manager.authenticate_user(
            db_test_connection,
            user_test_db.email,
            user_test_db_password
        )

        assert db_found_user is not None
        assert db_found_user.email == USER_DATA["email"]

