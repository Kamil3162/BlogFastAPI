from BlogFastAPI.app.schemas.post import PostCreate, PostRead
from BlogFastAPI.app.models.post import Post
from BlogFastAPI.app.models.user import User
from BlogFastAPI.app.models.category import PostCategory
from ..utils.deps import CustomHTTPExceptions
from ..utils.exceptions import NotFoundError
from sqlalchemy.orm import Session
from sqlalchemy import exc


class PostService:
    @staticmethod
    def check_post_existance(db: Session, title=None):
        try:
            return db.query(Post).filter(Post.title == title).first() is not None
        except exc.SQLAlchemyError:
            raise NotFoundError("Following post doesnt exists")

    @staticmethod
    def check_user_existance(db: Session, user_id):
        try:
            return db.query(User).filter(User.id == user_id).first() is not None
        except exc.SQLAlchemyError:
            raise NotFoundError("Following user doesnt exists")

    @staticmethod
    def create_post(post: PostCreate, db: Session):
        try:
            post_data = post
            if PostService.check_post_existance(db, post.title):
                # You can handle this by raising an exception or returning a message
                return CustomHTTPExceptions.bad_request()

            if PostService.check_user_existance(db, post_data.owner_id):
                return CustomHTTPExceptions.bad_request(
                    detail="A post with this title already exists"
                )

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
            raise CustomHTTPExceptions.internal_server_error()

    @staticmethod
    def update_post(post_id: int, post_data: PostCreate, db: Session) -> PostRead:
        """
            Function responsible for update post instance
        :param post_instance:
        :param post_data:
        :param db:
        :return:
        """
        post_instance = PostService.get_post(post_id, db)
        if not post_instance:
            raise CustomHTTPExceptions.not_found()

        for key, value in post_data.model_dump().items():
            setattr(post_instance, key, value)

        db.commit()
        db.refresh(post_instance)

        return PostRead.model_validate(post_instance)

    @staticmethod
    def delete_post(post_id: int, db: Session):
        try:
            post_instance = PostService.get_post(db, post_id)
            if not post_instance:
                raise CustomHTTPExceptions.not_found()

            db.delete(post_instance)
            db.commit()
            return {'status': 'deleted'}
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)

    @staticmethod
    def get_post(db: Session, post_id: int):
        try:
            post = db.query(Post).filter(Post.id == post_id).first()
            post.views += 1
            db.commit()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return post

    @staticmethod
    def get_posts(db: Session):
        try:
            posts = db.query(Post).all()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return posts

    @staticmethod
    def get_posts_range(db: Session, page_number=1):
        try:
            posts = db.query(Post).limit(10).offset(page_number)
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return posts

    @staticmethod
    def get_posts_by_category(db: Session, category_name):
        try:
            posts = db.query(Post) \
                .join(Post.categories) \
                .join(PostCategory) \
                .filter(PostCategory.category_name == category_name) \
                .all()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return posts

    @staticmethod
    def rate_post(mark, db: Session):
        pass

    @staticmethod
    def get_newest_post(db: Session):
        return db.query(Post).first()