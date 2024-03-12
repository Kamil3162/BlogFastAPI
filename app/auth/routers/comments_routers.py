from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.db.models.models import Comment
from BlogFastAPI.app.auth.schemas.comment_schemas import CommentScheme, CommentUpdate
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.auth.user_manager.user_auth import USER_AUTH
from BlogFastAPI.app.db.models.models import User
from .authentication_routers import oauth2_scheme
from BlogFastAPI.app.services.comment_service import CommentService

comment_routers = APIRouter()

@comment_routers.get("/comments")
async def get_comments(
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)):
    print("to jest endpoint comments")


@comment_routers.post("/comment-create")
async def comment_create(
        comment_data: CommentScheme,
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)):
    comment = CommentService.comment_create(comment_data, db)
    return comment


@comment_routers.put("/comment-update")
async def comment_update(
        comment_data: CommentUpdate,
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)
    ):
    comment = CommentService.check_existance(comment_data.comment_id, db)
    return comment

@comment_routers.delete("/comment-delete/{comment_id}")
async def comment_delete(
        comment_id,
        current_user: User = Depends(USER_AUTH.get_current_active_user),
        db: Session = Depends(get_db)
    ):
    CommentService.comment_delete(comment_id, db)
