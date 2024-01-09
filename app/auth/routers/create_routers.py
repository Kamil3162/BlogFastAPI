from fastapi import (
    HTTPException,
    Response,
    Request,
    APIRouter,
    status,
    Depends
)
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from BlogFastAPI.app.utils.utils import get_db, revoke_token
from ..schemas.post_schemas import PostCreate, PostRead, PostUpdate
from BlogFastAPI.app.db.models.models import User
from BlogFastAPI.app.services.post_service import PostService

from ..user_manager.user_auth import oauth2_scheme, USER_AUTH

create_post_router = APIRouter()
@create_post_router.post("/post-create/")
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    print("to jest post method do tworzenia posta ")
    created_post = PostService.create_post(post, db)
    return created_post

@create_post_router.put("/post-update/{post_id}/")
async def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(USER_AUTH.get_current_active_user)

):
    updated_post = PostService.update_post(post_id, post, db)
    return updated_post

@create_post_router.get("/post/{post_id}/")
async def post_detail(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    post = PostService.get_post(post_id, db)
    return post

@create_post_router.delete("/post-delete/{post_id}/")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(USER_AUTH.get_current_active_user)
):
    delete_status = PostService.delete_post(post_id, db)
    return delete_status