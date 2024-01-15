import pytest
from BlogFastAPI.app.services.post_service import PostService
from BlogFastAPI.app.services.user_service import UserService
from ..tests_auth.db_test import db_session

def test_create_post(db_session):
    # we need to validate owner_id doest it exist in our db
    user_id = 1

    post_data = {
        'title': 'test',
        'content': 'test',
        'photo_url': 'test@test',
        'owner_id': user_id
    }

    user_existance = UserService.get_user_by_id(db_session, user_id)
    user_permissions = UserService.check_post_create_permission(db_session, user_id)

    assert user_existance is not None
    assert user_permissions is not True

    created_post = PostService.create_post(post_data, db_session)

    assert created_post is not None
