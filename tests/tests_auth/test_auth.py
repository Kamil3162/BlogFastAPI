from fastapi.testclient import TestClient
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.auth.user_manager.user_auth import (
    USER_AUTH,
    UserAuth,
    oauth2_scheme
)
from .config import client

def test_email_user_duplication():
    """
        Function to check create user in db using the same data
    :return:
    """
    pass

def test_token_status():
    pass


def test_login():
    pass

def test_user_datamodel(): pass

def test_all_user_fields(): pass