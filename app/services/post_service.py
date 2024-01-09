from BlogFastAPI.app.auth.schemas.post_schemas import PostCreate, PostRead
from fastapi import HTTPException, status
from ..db.models.models import Post, User
from ..utils.utils import check_post_existance
from ..utils import exceptions
from sqlalchemy.orm import Session

class PostService:

    @staticmethod
    def check_post_existance(db: Session, title=None):
        return db.query(Post).filter(Post.title == title).first() is not None

    @staticmethod
    def check_user_existance(db: Session, user_id):
        return db.query(User).filter(User.id == user_id).first() is not None

    @staticmethod
    def create_post(post: PostCreate, db: Session):
        try:
            post_data = post
            if PostService.check_post_existance(db, post.title):
                # You can handle this by raising an exception or returning a message
                return exceptions.HTTP_POST_EXISTANCE_EXCEPTION

            if PostService.check_user_existance(db, post_data.owner_id):
                raise HTTPException(status_code=400, detail="A post with this title already exists")

            new_post = Post(
                title=post_data.title,
                content=post_data.content,
                photo_url=post_data.photo_url,
                owner_id=post_data.owner_id
            )

            db.add(new_post)
            db.commit()
            db.refresh(new_post)
            return new_post

        except Exception as e:
            # For example, log the error and/or re-raise the exception
            db.rollback()
            raise exceptions.HTTP_POST_SERVER_ERROR

    @staticmethod
    def update_post(post_id: int, post_data: PostCreate, db: Session) -> PostRead:
        """
            Function responsible for update post instance
        :param post_instance:
        :param post_data:
        :param db:
        :return:
        """
        post_instance = db.query(Post).filter(Post.id == post_id).first()
        if not post_instance:
            raise exceptions.HTTP_POST_EXCEPTION

        for key, value in post_data.model_dump().items():
            setattr(post_instance, key, value)

        db.commit()
        db.refresh(post_instance)

        return PostRead.model_validate(post_instance)

    @staticmethod
    def delete_post(post_id: int, db: Session):
        post_instance = db.query(Post).filter(Post.id == post_id).first()
        if not post_instance:
            raise exceptions.HTTP_POST_EXCEPTION

        db.delete(post_instance)
        db.commit()
        return {'status': 'deleted'}

    @staticmethod
    def get_post(post_id: int, db: Session):
        post = db.query(Post).filter(Post.id == post_id).first()
        return post