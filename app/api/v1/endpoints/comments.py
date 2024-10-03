from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from BlogFastAPI.app.schemas.comment import CommentScheme, CommentUpdate
from BlogFastAPI.app.utils.utils import get_db
from BlogFastAPI.app.models.user import User
from BlogFastAPI.app.services.comment import CommentService
from BlogFastAPI.app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/comments")
async def get_comments(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    print("to jest endpoint comments")


@router.post("/comment-create")
async def comment_create(
    comment_data: CommentScheme,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = CommentService.comment_create(comment_data, db)
    return comment


@router.put("/comment-update")
async def comment_update(
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = CommentService.check_existance(comment_data.comment_id, db)
    return comment

@router.delete("/comment-delete/{comment_id}")
async def comment_delete(
    comment_id,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    CommentService.comment_delete(comment_id, db)
