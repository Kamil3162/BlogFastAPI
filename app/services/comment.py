from typing import List

from BlogFastAPI.app.schemas.comment import CommentScheme
from sqlalchemy.orm import Session
from sqlalchemy import exc
from ..schemas.comment import (
    CommentScheme
)
from fastapi import HTTPException, status
from ..models.comment import Comment
from ..utils.utils import CustomHTTPExceptions
from ..utils.exceptions import NotFoundError
from ..db.repositories.post import PostRepository
from ..db.repositories.comments import CommentRepository
from ..exceptions.comment import CommentNotFound, PermissionDenied


class CommentService:
    def __init__(self, db):
        self._db = db
        self._post_repository = PostRepository(self._db)
        self._comment_repository = CommentRepository(self._db)

    def comment_create(self, comment_create: CommentScheme):
        try:
            post = PostRepository.get_by_id(self._db, comment_create.post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )
            comment_dict = comment_create.model_dump()
            comment = self._comment_repository.create(comment_dict)
            return comment
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def comment_update(self, comment: CommentScheme, user_id):
        try:
            comment_instance = self._comment_repository.get_by_id(comment.id)

            if not comment_instance:
                raise CommentNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )

            ownership = self._check_comment_ownership(
                comment_instance.id,
                user_id
            )

            if not ownership:
                raise PermissionDenied(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You havent access to change this"
                )
            updated_comment = self._comment_repository.update(
                comment_instance,
                comment
            )
            return CommentScheme.model_validate(updated_comment)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def comment_delete(self, comment_id, user_id):
        try:
            comment = self._comment_repository.get_by_id(comment_id)
            if not comment:
                raise CommentNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )

            ownership = self._check_comment_ownership(comment_id, user_id)

            if not ownership:
                raise PermissionDenied(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )

            self._comment_repository.delete(comment)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_comments_by_post_id(self, post_id) -> list[
        CommentScheme]:
        """
                Get all comments for a specific post
                """
        try:
            comments = self._comment_repository.get_comments_by_post_id(
                post_id
            )
            return [CommentScheme.model_validate(comment) for comment in
                    comments]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def _check_comment_ownership(
            self,
            comment_id: int,
            user_id: int,
    ) -> bool:
        try:
            comment = self._comment_repository.get_by_id(comment_id)
            if comment.commentator.id == user_id:
                return True
        except Exception as e:
            raise exc.DatabaseError(
                f"You havent access to modify this comment: str{e}"
            )
