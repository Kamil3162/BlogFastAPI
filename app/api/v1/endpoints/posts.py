import typing
from http.client import HTTPResponse
from typing import List, Optional

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ....utils.utils import get_db
from ....schemas.post import PostCreate, PostRead, PostUpdate, PostWithComments
from ....models.user import User
from ....services.post import PostService, PostViewService, PostVoteService
from ....services.users import UserService
from ....schemas.category import CategoryObject
from ....api.deps import (
    get_current_active_user,
    get_post_service,
    get_post_view_service,
    get_post_vote_service,

)
from ....core.enums import VoteType
from ....storage.files import file_service

router = APIRouter()
db = get_db()
post_service = PostService(db=db)

@router.get("/post/", response_model=PostWithComments)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    post_view_service: PostViewService = Depends(get_post_view_service),
    post_vote_service: PostVoteService = Depends(get_post_vote_service),
):
    post = post_service.get_post_with_comments(post_id)
    boolen = post_view_service.post_upview(post_id=post_id)
    up_post = post_vote_service.post_vote_operation(
        user_id=1,
        post_id=post_id,
        vote_type=VoteType.DOWNVOTE,
    )

    return PostWithComments.model_validate(post)

@router.get("/post/{post_id}/")
async def upvote_post(
    post_id: int,
    vote: int,
    #current_user: User = Depends(get_current_active_user),
    post_vote_service: PostVoteService = Depends(get_post_vote_service),
):
    post_vote = post_vote_service.post_vote_operation(
        user_id=1,
        post_id=post_id,
        vote_type=VoteType(vote),
    )

    return JSONResponse(
        status_code=200,
        content="Proper post upvote",
    )

@router.get("/post-test/{post_id}/", response_model=PostRead)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    post_view_service: PostViewService = Depends(get_post_view_service),
    # current_user: User = Depends(get_current_active_user)
):
    post = post_service.get_post_with_comments(post_id)
    # post_view_service.get_post_with_comments(1, post_id, )
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
    return post_service.get_post_list(page=page, limit=10)

@router.delete("/post-delete/{post_id}/")
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    # current_user: User = Depends(get_current_active_user)
):
    delete_status = post_service.delete_post(post_id)
    return delete_status

@router.get("/posts/category")
async def get_posts_by_category(
    category_id: int,
    post_service: PostService = Depends(get_post_service),
    #user: User = Depends(get_current_active_user)
):
    posts = post_service.get_posts_by_category(category_id)
    return posts





