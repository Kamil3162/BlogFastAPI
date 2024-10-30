from sqlalchemy.orm import Session
from sqlalchemy import exc
from ..schemas.comment import (
    CommentScheme
)
from ..models.comment import Comment
from ..services.post import PostService
from ..utils.utils import CustomHTTPExceptions
from ..utils.exceptions import NotFoundError
class CommentService:
    @staticmethod
    def comment_create(comment_create: CommentScheme, db: Session):
        try:
            # eventually post title
            post_id = comment_create.post_id

            if PostService.check_post_existance(db, post_id):
                return CustomHTTPExceptions.bad_request()

            comment = Comment(
                post_id=post_id,
                content=comment_create.content,
                commentator_id=comment_create.commentator_id
            )
        except Exception as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment

    @staticmethod
    def check_existance(comment_id, db: Session):
        try:
            comment = db.query(Comment). \
                       filter(Comment.id == comment_id).first()
        except exc.SQLAlchemyError:
            raise NotFoundError("Following user doesnt exists")
        else:
            return comment

    @staticmethod
    def comment_update(comment: CommentScheme, db: Session):
        comment_id = comment.id
        comment_instance = CommentService.check_existance(comment_id, db)

        for key, value in comment.model_dump().items():
            setattr(comment_instance, key, value)

        db.commit()
        db.refresh(comment_instance)

        return CommentScheme.model_validate(comment_instance)

    @staticmethod
    def comment_delete(comment_id, db: Session):
        comment_instance = CommentService.check_existance(comment_id, db)
        db.delete(comment_instance)
        db.commit()
        return {'status': 'deleted'}

    @staticmethod
    def get_comments_by_post_id(post_id, db: Session):
        comments_instance = db.execute(Comment).where(Comment.post_id == post_id)
        return comments_instance