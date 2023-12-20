from fastapi.testclient import TestClient
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.auth.user_manager.user_auth import (
    USER_AUTH,
    UserAuth,
    oauth2_scheme
)
from .config import client

# i have to check does user is created
# check does we can log in with this data or soemthing like this
# check get hash password function
# check duplication of emails in our db
# sprawdzic checker z szukaniem usersow

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

def test_create_user_success():
    user_payload = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    db_test_connection = SessionLocal()

    db_user = db_test_connection.query(User).filter(
        User.email == user_payload["email"]
    ).first()

    assert db_user is None
    db_test_connection.close()


def test_user_create():
    user_payload = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    }

    with SessionLocal() as db_test_connection:
        user_db = db_test_connection.query(User).filter(
            User.email == user_payload["email"]
        )

        assert user_db is None

        user_plain_password = user_payload["password"]
        user = User(**user_payload)

        hashed_user_password = user_auth_manager.get_hash_password(
            user_plain_password
        )

        user.hashed_password = hashed_user_password

        db_test_connection.add(User)
        db_test_connection.commit()
        db_test_connection.close()

        created_user = db_test_connection.query(User).filter(
            User.email == user_payload["email"]
        ).first()

        assert created_user is not None
        assert created_user.email == user_payload["email"]



