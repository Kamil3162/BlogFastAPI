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
from ....api.deps import get_current_active_user

router = APIRouter()
db = get_db()
post_service = PostService(db=db)

@router.get("/post/{post_id}/", response_model=PostWithComments)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService.get_post_with_comments(post_id)
    return PostWithComments.model_validate(post)

@router.get("/post-test/{post_id}/", response_model=PostRead)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService.get_post_with_comments(post_id)
    return PostWithComments.model_validate(post)


@router.get("/posts", response_model=List[PostRead])
async def get_posts(
    page: int = Query(1, gt=0),
    q: Optional[str] = None,
    # current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):

    all_posts = PostService.get_posts_paginated(page=page, limit=10)
    return all_posts

@router.get("/newest-post")
async def get_newest_post(db: Session = Depends(get_db)):
    post = post_service.get_newest_post()
    return post

@router.post("/post-create/")
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = UserService.get_user_by_id(db, post.owner_id)
    created_post = PostService.create_post(post, user)
    return created_post

@router.put("/post-update/{post_id}/")
async def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> typing.Any:
    """
    Update an existing post.

    Args:
        post_id: The ID of the post to update
        post: The updated post data
        db: Database session
        current_user: The authenticated user

    Returns:
        PostResponse: The updated post

    Raises:
        HTTPException:
            - 404: Post not found
            - 403: User doesn't have permission to update this post
            - 401: User is not authenticated
    """
    updated_post = PostService.update_post(post_id, post, db)
    return updated_post

@router.get("/post-list")
async def post_list(
    page: int = Query(1, gt=0)
):
    pass

@router.delete("/post-delete/{post_id}/")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    delete_status = PostService.delete_post(post_id=post_id)
    return delete_status



