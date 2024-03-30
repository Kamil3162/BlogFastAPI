from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.auth.user_manager.user_auth import (
    UserAuth,
    oauth2_scheme
)
from BlogFastAPI.tests.test_configs.db_test import db_session
from BlogFastAPI.tests.test_configs.config import client


USER_DATA = {
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "password123"
}

user_auth_manager = UserAuth(oauth2_scheme)

def test_get_method():
    """
        Function to check does method according to register will work on get method
    :return:
    """
    response = client.get("/register")
    assert response.status_code == 405

def test_create_user_success(db_session):
    user_payload = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    db_user = db_session.query(User).filter(
        User.email == user_payload["email"]
    ).first()

    assert db_user is None
    db_session.close()


def test_user_create(db_session):
    user_payload = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    user_db = db_session.query(User).filter(
        User.email == user_payload["email"]
    )

    assert user_db is None

    user_plain_password = user_payload["password"]
    user = User(**user_payload)

    hashed_user_password = user_auth_manager.get_hash_password(
        user_plain_password
    )

    user.hashed_password = hashed_user_password

    db_session.add(User)
    db_session.commit()
    db_session.close()

    created_user = db_session.query(User).filter(
        User.email == user_payload["email"]
    ).first()

    assert created_user is not None
    assert created_user.email == user_payload["email"]



