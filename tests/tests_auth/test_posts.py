import pytest
from .db_test import db_session
from .config import client

def test_get_post(db_session):
    # check response of post
    response = client.get("/post/1/")
    assert response.status_code == 200

def test_get_nonexistent_post():
    # Request a post with an ID that doesn't exist
    response = client.get("/post/99999/")
    assert response.status_code == 404

def test_create_post(db_session):
    # first we have to check does we have a permission tro create a new post
    post_data = {
        'title': 'test',
        'content': 'test',
        'photo_url': 'test@test',
        'owner_id': 3
    }


def test_update_post():
    pass

def test_delete_post():
    pass