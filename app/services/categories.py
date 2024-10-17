from sqlalchemy.orm import Session
from sqlalchemy import exc
from ..models.post import Post
from ..utils.deps import CustomHTTPExceptions
from ..models.category import PostCategory
from ..schemas.category import (
    CategoryScheme
)

class CategoryService:
    @staticmethod
    def get_by_category(db: Session, *categories):
        try:
            posts = db.query(Post).filter(Post.category.in_(categories))
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return posts

    @staticmethod
    def get_category_by_id(db: Session, category_id):
        try:
            return db.query(PostCategory).filter(
                PostCategory.id == category_id
            ).first()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)


    @staticmethod
    def all_categories(db: Session):
        try:
            categories = db.query(PostCategory).all()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return categories

    @staticmethod
    def check_category_existence(db: Session, category_named):
        try:
            return db.query(PostCategory).filter(
                   PostCategory.category_name == category_named
            ).first()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exeception(e)
            return False

    @staticmethod
    def create_category(db: Session, category_scheme: CategoryScheme):
        try:
            category_name = category_scheme.category_name
            category = CategoryService.check_category_existence(
                db, category_name
            )

            if category:
                return False
            category_created = PostCategory(category_name=category_name)

            db.add(category_created)
            db.commit()
        except Exception as e:
            CustomHTTPExceptions.handle_db_exeception(e)
        else:
            return category_created

    @staticmethod
    def category_delete(db: Session, category_id):
        try:
            category = CategoryService.get_category_by_id(db, category_id)
            if not category:
                return False

            db.delete(category)
            db.commit()

            return True
        except exc.SQLAlchemyError as e:
            db.rollback()
            CustomHTTPExceptions.handle_db_exeception(e)
            return False

    @staticmethod
    def category_update(
            category_id,
            db: Session,
            category_data: CategoryScheme
        ):
        category = CategoryService.get_category_by_id(db, category_id)
        category.category_name = category_data.category_name

        db.commit()
        db.refresh(category)

        return category