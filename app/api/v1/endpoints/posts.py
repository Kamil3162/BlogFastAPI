from typing import List, Optional

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.schemas.post import PostCreate, PostRead, PostUpdate
from BlogFastAPI.app.models.user import User
from BlogFastAPI.app.models.post import Post
from BlogFastAPI.app.services.post import PostService
from BlogFastAPI.app.services.users import UserService
from BlogFastAPI.app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/post/{post_id}/", response_model=PostRead)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService.get_post(db, post_id)
    return PostRead.model_validate(post)

@router.get("/posts", response_model=List[PostRead])
async def get_posts(
    page: int = Query(1, gt=0),
    q: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):

    all_posts = PostService.get_posts_range(db, page)
    return all_posts

@router.get("/posts/statistic", response_model=List[PostRead])
async def fetch_post_data(
    page: int = Query(1, gt=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    posts = db.query(Post).limit(20).offset(page)
    for post in posts:
        print(post)

@router.get("/newest-post")
async def get_newest_post(db: Session = Depends(get_db)):
    post = PostService.get_newest_post(db)
    return post

@router.post("/post-create/")
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    print(post)
    user = UserService.get_user_by_id(db, post.owner_id)
    created_post = PostService.create_post(post, db)
    return created_post

@router.put("/post-update/{post_id}/")
async def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
        Update a post.
    """
    updated_post = PostService.update_post(post_id, post, db)
    return updated_post

@router.delete("/post-delete/{post_id}/")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    delete_status = PostService.delete_post(post_id, db)
    return delete_status



