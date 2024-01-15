from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.db.database import SessionLocal
from BlogFastAPI.app.db.models.models import Comment
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.auth.user_manager.user_auth import USER_AUTH
from BlogFastAPI.app.db.models.models import User
from .authentication_routers import oauth2_scheme

comment_routers = APIRouter()

@comment_routers.get("/comments")
async def get_comments(
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)):
    print("to jest endpoint comments")

@comment_routers.post("/comment-create/{post_id}/")
async def comment_create(
        # function responsible for create new comment for particular post_id
    post_id: int,
    current_user: User = Depends(USER_AUTH.get_current_active_user),
    db: Session = Depends(get_db)):
    print(post_id)
