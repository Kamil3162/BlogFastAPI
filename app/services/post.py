from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    DataError,
    NoResultFound
)


from ..db.repositories.post import PostRepository
from ..schemas.post import PostCreate, PostRead, PostWithComments
from ..services.comment import CommentService
from ..exceptions.post import PostNotFound
from ..models.post import Post


class PostService:
    def __init__(self, db: Session):
        self._db = db
        self._repository = PostRepository()
        self._comment_service = CommentService(db)

    def get_post_by_id(self, post_id: int) -> PostRead:
        """
        Get post by ID with error handling
        """
        try:
            post = self._repository.get_by_id(self._db, post_id)
            if not post:
                raise PostNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    description="Post not found"
                )
            return PostRead.model_validate(post)
        except PostNotFound as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.description
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def check_post_existence(self, title: str) -> bool:
        """
        Check if post exists by title.
        Let the global handlers manage the specific database errors.
        """
        if not title:
            raise DataError("Title cannot be empty")

        post = self._repository.get_by_title(self._db, title.strip())
        if not post:
            raise NoResultFound()


    def create_post(self, post_data: PostCreate, user_id: int) -> PostRead:
        """
        Create new post with validation
        """
        try:
            # Check if post with same title exists
            if self.check_post_existence(post_data.title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Post with this title already exists"
                )

            # Create post
            post = self._repository.create(
                self._db,
                post_data,
                user_id
            )
            return PostRead.model_validate(post)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def update_post(
            self,
            post_id: int,
            post_data: PostCreate,
            user_id: int
    ) -> PostRead:
        """
        Update post with ownership verification
        """
        try:
            # Get post
            post = self._repository.get_by_id(self._db, post_id)
            if not post:
                raise PostNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    description="Post not found"
                )

            # Verify ownership
            if post.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this post"
                )

            # Update post
            updated_post = self._repository.update(
                post,
                post_data,
                self._db
            )
            return PostRead.model_validate(updated_post)
        except (PostNotFound, HTTPException):
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_posts_paginated(
            self,
            page: int = 1,
            limit: int = 10
    ) -> List[PostRead]:
        """
        Get paginated posts
        """
        try:
            skip = (page - 1) * limit
            posts = self._repository.get_posts_range(
                self._db,
                skip=skip,
                limit=limit
            )
            return [PostRead.model_validate(post) for post in posts]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_posts_by_category(
            self,
            category_name: str
    ) -> List[PostRead]:
        """
        Get all posts in a category
        """
        try:
            posts = self._repository.get_by_category(
                self._db,
                category_name
            )
            return [PostRead.model_validate(post) for post in posts]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_post_with_comments(self, post_id: int) -> PostWithComments:
        """
        Get post with its comments
        """
        try:
            post = self._repository.get_by_id(self._db, post_id)
            if not post:
                raise PostNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    description="Post not found"
                )

            comments = self._comment_service.get_comments_by_post_id(post_id)

            return PostWithComments(
                post=PostRead.model_validate(post),
                comments=comments
            )
        except PostNotFound as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.description
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_newest_post(self) -> Optional[PostRead]:
        """
        Get the newest post
        """
        try:
            post = self._repository.get_newest_post(self._db)
            return PostRead.model_validate(post) if post else None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )