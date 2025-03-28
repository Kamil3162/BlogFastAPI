import typing
from typing import List, Optional

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ....utils.utils import get_db
from ....schemas.post import PostCreate, PostRead, PostUpdate, PostWithComments
from ....models.user import User
from ....services.post import PostService
from ....services.users import UserService
from ....schemas.category import CategoryObject
from ....api.deps import get_current_active_user, get_post_service

router = APIRouter()
db = get_db()
post_service = PostService(db=db)

@router.get("/post/", response_model=PostWithComments)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service)
):
    post = post_service.get_post_with_comments(post_id)
    return PostWithComments.model_validate(post)

@router.get("/post-test/{post_id}/", response_model=PostRead)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    # current_user: User = Depends(get_current_active_user)
):
    post = post_service.get_post_with_comments(post_id)
    return PostWithComments.model_validate(post)


@router.get("/posts", response_model=List[PostRead])
async def get_posts(
    page: int = Query(1, gt=0),
    post_service: PostService = Depends(get_post_service),
        q: Optional[str] = None,
    # current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):

    all_posts = post_service.get_posts_paginated(page=page, limit=10)
    return all_posts

@router.get("/newest-post")
async def get_newest_post(
    post_service: PostService = Depends(get_post_service)
):
    post = post_service.get_newest_post()
    return post

@router.post("/post-create/")
async def create_post(
    post_data: PostCreate,
    category_data: CategoryObject,
    service: PostService = Depends(get_post_service),
    # current_user: User = Depends(get_current_active_user)
):
    created_post = service.create_post(post_data, category_data)
    return created_post

@router.put("/post-update/")
async def update_post(
    post_data: PostUpdate,
    service: PostService = Depends(get_post_service),
    # current_user: User = Depends(get_current_active_user)
) -> typing.Any:

    """
    Update an existing post.

    Args:
        post_data: Data scheme for update post
        service: Service class with all possible operations on post data
        current_user: The authenticated user

    Returns:
        PostResponse: The updated post

    Raises:
        HTTPException:
            - 404: Post not found
            - 403: User doesn't have permission to update this post
            - 401: User is not authenticated
    """
    user_id = 1

    updated_post = service.update_post(post_data, user_id)
    return updated_post

@router.get("/post-list/")
async def post_list(
    page: int = Query(1, gt=0),
    post_service: PostService = Depends(get_post_service),
):
    print(page)
    return post_service.get_post_list(page=page, limit=10)

@router.delete("/post-delete/{post_id}/")
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    # current_user: User = Depends(get_current_active_user)
):
    delete_status = post_service.delete_post(post_id)
    return delete_status



