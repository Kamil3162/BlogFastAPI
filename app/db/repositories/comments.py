import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import exc

from ...models.comment import Comment
from ...schemas.comment import CommentBaseScheme


class CommentRepository:

    def __init__(self, db: Session):
        self._db = db

    def create(self, comment_data: dict) -> Comment:
        comment = Comment(**comment_data)
        self._db.add(comment)
        self._db.commit()
        self._db.refresh(comment)
        return comment

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Retrieve a comment by ID"""
        return (
            self._db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def update(self, comment: Comment, update_data: dict) -> Comment:
        """Update comment attributes"""
        for key, value in update_data.items():
            setattr(comment, key, value)
        comment.updated_at = datetime.datetime.utcnow()
        return comment

    def delete(self, comment_data: CommentBaseScheme) -> bool:
        """
            Delete a comment
        """
        result = self._db.query(Comment). \
            filter(Comment.id == comment_data.id).delete()
        return bool(result)

    def get_comments_by_post_id(self, post_id: int) -> List[Comment]:
        return self._db.query(Comment) \
            .filter(Comment.post_id == post_id) \
            .all()
