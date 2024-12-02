import typing

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.post import Post
from ..models.category import PostCategory, PostCategories
from ..db.repositories.posts_categories import PostsCategoriesRepository
from ..schemas.category import CategoryPostObject

# exceptions.py

class CategoryAssignmentError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class CategoryNotFoundError(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )

class PostNotFoundError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

class CategoryAlreadyAssignedError(HTTPException):
    def __init__(self, post_id: int, category_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category {category_id} is already "
                   f"assigned to post {post_id}"
        )

class PostsCategoriesService:
    def __init__(self, db: Session):
        self._db = db
        self._repository = PostsCategoriesRepository(self._db)

    def assign_category_to_post(
            self,
            post_id: int,
            category_id: int
    ) -> CategoryPostObject:
        """
        Assign a category to a post.

        Args:
            post_id: Post ID
            category_id: Category ID

        Returns:
            CategoryResponse: Assigned category data

        Raises:
            CategoryAlreadyAssignedError: If category is already assigned to post
            SQLAlchemyError: If database operation fails
        """
        try:
            # Check if already assigned
            existing = self._repository.filter_assigned_categories_to_post(
                post_id=post_id,
                category_id=category_id
            )


            if existing:
                raise CategoryAlreadyAssignedError(post_id, category_id)

            result = self._repository.assign_category_to_post(
                post_id=post_id,
                category_id=category_id
            )

            return CategoryPostObject.model_validate(result)

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign category to post"
            )

    def get_post_categories(
            self,
            post: Post
    ) -> typing.List[CategoryPostObject]:
        """
        Get all categories assigned to a post.

        Args:
            post: Post instance

        Returns:
            List[CategoryResponse]: List of assigned categories

        Raises:
            PostNotFoundError: If post doesn't exist
            SQLAlchemyError: If database operation fails
        """
        try:
            categories = self._repository.get_assigned_category_to_post(post)
            return [
                CategoryPostObject.model_validate(cat) for cat in categories
            ]

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch post categories"
            )

    def update_post_category(
            self,
            post: Post,
            category: PostCategory
    ) -> bool:
        """
        Update category assignment for a post.

        Args:
            post: Post instance
            category: New category instance

        Returns:
            bool: True if update was successful

        Raises:
            CategoryNotFoundError: If category assignment doesn't exist
            SQLAlchemyError: If database operation fails
        """
        try:
            result = self._repository.update_assigned_category_for_post(
                post=post,
                category=category
            )

            if not result:
                raise CategoryNotFoundError(category.id)

            return True

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update post category"
            )

    def remove_category_from_post(
            self,
            post: Post,
            category: PostCategory
    ) -> bool:
        """
        Remove category assignment from a post.

        Args:
            post: Post instance
            category: Category instance to remove

        Returns:
            bool: True if removal was successful

        Raises:
            CategoryNotFoundError: If category assignment doesn't exist
            SQLAlchemyError: If database operation fails
        """
        try:
            result = self._repository.remove_category_from_post(
                post=post,
                category=category
            )

            if not result:
                raise CategoryNotFoundError(category.id)

            return True

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove category from post"
            )