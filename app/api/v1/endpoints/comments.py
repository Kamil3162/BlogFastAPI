from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ....schemas.comment import CommentScheme, CommentUpdate
from ....utils.utils import get_db
from ....models.user import User
from ....services.comment import CommentService
from ....api.deps import get_current_active_user
from ...deps import get_comment_service

router = APIRouter()


@router.post("/comment-create")
async def comment_create(
    comment_data: CommentScheme,
    #current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    comment_data.commentator_id = 1
    comment = comment_service.comment_create(comment_data)
    return comment


@router.put("/comment-update")
async def comment_update(
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    comment = comment_service.comment_update(comment_data, current_user.id)
    return comment

@router.delete("/comment-delete/{comment_id}")
async def comment_delete(
    comment_id,
    current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    comment = comment_service.comment_delete(comment_id, current_user.id)
    return comment