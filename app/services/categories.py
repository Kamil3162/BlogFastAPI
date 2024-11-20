from sqlalchemy.orm import Session
from sqlalchemy import exc

from ..models.post import Post
from ..utils.deps import CustomHTTPExceptions
from ..models.category import PostCategory
from ..schemas.category import (
    CategoryScheme
)
from ..db.repositories.categories import CategoryRepository
from ..schemas.category import CategoryObject

class CategoryService:
    def __init__(self, db: Session):
        self._db = db
        self.model = PostCategory
        self._repository = CategoryRepository(self._db)

    def get_posts_by_category(self, category_data: CategoryObject):
        posts = self._db.query(Post) \
                 .filter(Post.category.category_name == category_data.category_name)

        if not posts:
            raise Exception("No posts with following category name")

        return posts

    def get_category_by_id(self, category_id):
        category = self._repository.get_by_id(category_id)

        if not category:
            raise Exception("following Category doesnt exsists")

        return category

    def all_categories(self):
        try:
            categories = self._repository.get_all_categories()
        except exc.SQLAlchemyError as e:
            CustomHTTPExceptions.handle_db_exceptiopn(e)
        else:
            return categories

    def create_category(self, category_scheme: CategoryScheme):
        try:
            category_name = category_scheme.category_name
            category = self._repository.get_category_by_name(category_name)

            if category:
                return False
            category_created = PostCategory(category_name=category_name)

            self._db.add(category_created)
            self._db.commit()
        except Exception as e:
            CustomHTTPExceptions.handle_db_exceptiopn(e)
        else:
            return category_created

    def category_delete(self, category_id):
        try:
            category = self._repository.get_by_id(category_id)
            if not category:
                return False

            self._db.delete(category)
            self._db.commit()
            return True

        except exc.SQLAlchemyError as e:
            self._db.rollback()
            CustomHTTPExceptions.handle_db_exceptiopn(e)
            return False

    def category_update(
            self,
            category_data: CategoryObject
    ) -> CategoryObject:
        category = self._repository.get_by_id(category_data.id)
        category.category_name = category_data.category_name

        self._db.commit()
        self._db.refresh(category)

        category_scheme = CategoryObject(
            id=category.id,
            category_name=category.category_name
        )

        return category_scheme
