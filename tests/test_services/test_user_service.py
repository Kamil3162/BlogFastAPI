import pytest
from BlogFastAPI.app.services.user_service import UserService
from BlogFastAPI.app.utils.exceptions import CustomHTTPExceptions
from BlogFastAPI.app.auth.user_manager.user_auth import UserAuth
from ..tests_auth.db_test import db_session
def test_create_user(db_session):
    password = "password123"

    user_payload = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "hashed_password": UserAuth.get_hash_password(password)}

    user = UserService.create_user(db_session, user_payload)

    assert user is not None
    assert user.email == user_payload["email"]
    assert user.first_name == user_payload["email"]
    assert user.last_name == user_payload["email"]

def test_blacklisted_users(db_session): pass

def test_user_existancce(db_session): pass

def test_get_user_id_success(db_session):
    # test function to get user using id
    valid_user_id = 1

    user = UserService.get_user_by_id(db_session, valid_user_id)
    assert user is not None
    assert user.id == valid_user_id

def test_get_user_id_failed(db_session):
    user_id = 321321
    user = UserService.get_user_by_id(db_session, user_id)
    assert user is None

def test_get_user_by_id_not_found(db_session):
    # Use an ID that does not exist in your test database
    non_existent_user_id = 9999
    with pytest.raises(CustomHTTPExceptions.not_found) as exc_info:
        UserService.get_user_by_id(db_session, non_existent_user_id)

    # Optionally, check the exception message
    assert str(
        exc_info.value) == f"User with ID:{non_existent_user_id} not found"