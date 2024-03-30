from BlogFastAPI.tests.test_configs.db_test import db_session
from BlogFastAPI.tests.test_configs.user_for_test import client

def test_get_post(db_session, client):
    # check response of post
    response = client.get("/post/1/")
    assert response.status_code == 200

def test_get_nonexistent_post(client):
    # Request a post with an ID that doesn't exist
    response = client.get("/post/99999/")
    assert response.status_code == 404

def test_create_post(db_session):
    pass

def test_update_post():
    pass

def test_delete_post():
    pass