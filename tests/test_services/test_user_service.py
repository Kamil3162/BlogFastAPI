import pytest
from fastapi import HTTPException

from BlogFastAPI.app.services.users import UserService
from BlogFastAPI.app.core.security import USER_AUTH
from BlogFastAPI.tests.test_configs.db_test import db_session


def test_create_user(db_session):
    password = "password"

    user_payload = {
        "email": "test1@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "hashed_password": USER_AUTH.get_hash_password(password)}

    user = UserService.create_user(db_session, user_payload)

    assert user is not None
    assert user.email == user_payload["email"]
    assert user.first_name == user_payload["email"]
    assert user.last_name == user_payload["email"]

def test_blacklisted_users(db_session): pass

def test_user_existanse(db_session): pass

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
    non_existent_user_id = 9999
    with pytest.raises(HTTPException) as exc_info:
        UserService.get_user_by_id(db_session, non_existent_user_id)

    assert str(exc_info.value.detail) == f"User with ID:{non_existent_user_id} not found"
