from sqlalchemy.orm import Session
from sqlalchemy import exc

from fastapi import HTTPException, status

from ..models.post import Post
from ..utils.deps import CustomHTTPExceptions
from ..models.category import PostCategory
from ..schemas.category import (
    CategoryScheme
)
from ..db.repositories.categories import CategoryRepository
from ..schemas.category import CategoryObject, CategoryResponse

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
            raise
        else:
            return categories

    def create_category(self, category_scheme: CategoryScheme):
        try:
            category_name = category_scheme.category_name

            created_category = self._repository.create_category(
                category_name=category_name
            )

            parsed_data = CategoryObject.model_validate(created_category)

            return CategoryResponse(
                success=True,
                message="Category created successfully",
                data=parsed_data
            )
        except exc.IntegrityError:
            self._db.rollback()
            raise exc.IntegrityError

    def category_delete(self, category_id):
        try:
            deleted_category = self._repository.delete_category(
                category_id
            )

            if not deleted_category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID {category_id} not found"
                )

            return CategoryObject(
                id=deleted_category.id,
                category_name=deleted_category.category_name
            )

        except exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete category with existing references"
            )
        except exc.SQLAlchemyError:
            raise

    def category_update(
            self,
            category_data: CategoryObject
    ) -> CategoryResponse:
        category = self._repository.update_category(
            category_data.id, category_data
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category.id} not found"
            )

        parsed_data = CategoryObject.model_validate(category)

        return CategoryResponse(
            success=True,
            message="Category updated successfully",
            data=parsed_data
        )
