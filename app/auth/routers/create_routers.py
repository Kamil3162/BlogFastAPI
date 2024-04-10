from fastapi import (
    HTTPException,
    Response,
    Request,
    APIRouter,
    status,
    Depends
)
from typing import List, Optional
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.utils.utils import get_db, revoke_token
from ..schemas.post_schemas import PostCreate, PostRead, PostUpdate
from BlogFastAPI.app.db.models.models import User, Post
from BlogFastAPI.app.services.post_service import PostService
from BlogFastAPI.app.services.user_service import UserService
from BlogFastAPI.app.auth.user_manager.user_auth import oauth2_scheme, USER_AUTH
from BlogFastAPI.app.utils.decorators import check_db_operations, check_data_key

create_post_router = APIRouter()

@check_data_key
@check_db_operations
@create_post_router.get("/post/{post_id}/", response_model=PostRead)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService.get_post(db, post_id)
    return PostRead.model_validate(post)

# @check_db_operations
@create_post_router.get("/posts/{page_number}", response_model=List[PostRead])
async def get_posts(
        page_number: str,
        q: Optional[str] = None,
        page: int = 1,
        # current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)
):
    print(page_number)
    print(q)
    print(page)
    all_posts = PostService.get_posts_range(db, page)
    return all_posts


@check_db_operations
@create_post_router.post("/post-create/")
async def create_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    user = UserService.get_user_by_id(db, post.owner_id)
    created_post = PostService.create_post(post, db)
    return created_post

@check_data_key
@check_db_operations
@create_post_router.put("/post-update/{post_id}/")
async def update_post(
        post_id: int,
        post: PostUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(USER_AUTH.get_current_active_user)

):
    updated_post = PostService.update_post(post_id, post, db)
    return updated_post
@check_data_key
@check_db_operations
@create_post_router.delete("/post-delete/{post_id}/")
async def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    delete_status = PostService.delete_post(post_id, db)
    return delete_status


