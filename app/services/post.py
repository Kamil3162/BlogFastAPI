from typing import List, Optional, Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    DataError,
    NoResultFound,
    DatabaseError
)
from decimal import Decimal

from ..schemas.user import UserResponse
from ..db.repositories.post import PostRepository
from ..schemas.post import PostCreate, PostRead, PostWithComments, PostDelete,\
    PostShortInfo, PostUpdate
from ..schemas.category import CategoryObject, CategoryScheme
from ..services.comment import CommentService
from ..services.categories import CategoryService
from ..services.users import UserService
from ..services.posts_categories import PostsCategoriesService
from ..exceptions.post import PostNotFound
from ..db.repositories.posts_categories import PostsCategoriesRepository
from ..models.post import Post, PostView, PostVote
from ..core.enums import VoteType
from ..core.enums import PostEarning

class PostService:
    def __init__(self, db: Session):
        self._db = db
        self._repository = PostRepository(self._db)
        self._comment_service = CommentService(self._db)
        self._category_service = CategoryService(self._db)
        self._posts_categories = PostsCategoriesService(self._db)
        self._post_view_service = PostViewService(self._db)

    def get_post_by_id(self, post_id: int) -> PostRead:
        """
        Get post by ID with error handling
        """
        try:
            post = self._repository.get_by_id(post_id)
            if not post:
                raise PostNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    description="Post not found"
                )
            self._post_view_service.post_upview(post_id=post_id)
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
            return False
        else:
            return True

    def create_post(
        self,
        post_data: PostCreate,
        category_data: CategoryObject,
    ) -> PostRead:
        """
        Create new post with validation
        """
        try:
            category = self._category_service.get_category_by_id(
                category_id=category_data.id
            )

            # Check if post with same title exists
            if self.check_post_existence(post_data.title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Post with this title already exists"
                )

            # Create post
            post = self._repository.create(
                post_data,
            )

            self._posts_categories.assign_category_to_post(
                post.id, category_data.id
            )

            return PostRead.model_validate(post)
        # except HTTPException:
        #     raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{str(e)}"
            )

    def update_post(
            self,
            post_data: PostUpdate,
            user_id: int
    ) -> PostRead:
        """
        Update post with ownership verification
        """
        try:
            # Get post
            post_id = post_data.id

            post = self._repository.get_by_id(post_id)

            if not post:
                raise PostNotFound(
                    status_code=status.HTTP_404_NOT_FOUND,
                    description="Post not found"
                )

            # Verify ownership
            if post.owner_id is not user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this post"
                )

            # Update post
            updated_post = self._repository.update(
                post,
                post_data,
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
            print(posts[0])
            return [PostRead.model_validate(post) for post in posts]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_posts_by_category(
            self,
            category_id: int
    ) -> List[PostRead]:
        """
        Get all posts in a category
        """
        try:
            posts = self._repository.get_by_category(
                self._db,
                category_id,
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
            post = self._repository.get_by_id(post_id)
            print(post)

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

    def delete_post(self, post_id: int):
        """
            Delete post using post_id
        """
        try:
            was_deleted = self._repository.delete_post(post_id)

            if not was_deleted:
                raise PostNotFound(f"Post with id:{post_id} not found")

            self._db.commit()

            return PostDelete(
                id=post_id,
                description=f"Post {post_id} successfully deleted"
            )
        except SQLAlchemyError as e:
            self._db.rollback()
            raise DatabaseError(f"Database error: {str(e)}")

    def get_post_list(self, page: int, limit: int):
        try:
            skip = (page - 1) * limit
            posts = self._repository.get_posts_range(
                self._db,
                skip=skip,
                limit=limit
            )
            """
                #category=CategoryScheme(
                    #    category_name=post.post_categories[
                   #         0].category.category_name if post.post_categories else ""
                   # ),
            """
            return [
                PostShortInfo(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    owner=UserResponse(
                        id=post.owner.id,
                        email=post.owner.email,
                        first_name=post.owner.first_name,
                        last_name=post.owner.last_name,
                        is_active=post.owner.is_active
                    )
                )
                for post in posts
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

class PostVoteService:
    def __init__(self, db: Session):
        self._db = db
        self._post_service = PostService(self._db)
        self._user_service = UserService(self._db)
        self._post_repository = PostRepository(self._db)

    def post_vote_operation(self, user_id, post_id, vote_type: VoteType):
        try:
            user = self._user_service.get_user_by_id(user_id)
            post = self._post_service.get_post_by_id(post_id)

            post_vote = self._post_repository.get_vote_instance(
                user_id=user.id,
                post_id=post.id,
            )

            if not post_vote:
                vote = self._post_repository.upvote_create(
                    user_id=user.id,
                    post_id=post.id,
                    vote_type=vote_type
                )
            else:
                post_vote.vote_type = vote_type

            self._db.commit()

            return True
        except Exception as e:
            raise e

    def post_vote_update(
        self,
        user_id,
        post_id: int,
        vote_type: VoteType
    ):
        vote_instance = self._post_repository.upvote_update(
            post_id=post_id,
            user_id=user_id,
            vote_type=vote_type
        )

        return vote_instance

class PostViewService:
    def __init__(self, db: Session):
        self._db = db
        self._user_repository = UserService(self._db)
        self._repository = PostsCategoriesRepository(self._db)
        self._post_repository = PostRepository(self._db)

    def post_upview(self, post_id: int, user_id: int = 1,
                    user_ip: str = "") -> bool:
        """
        Record a view for a post.

        Args:
            post_id: ID of the post to view
            user_id: ID of the viewing user (defaults to 1)
            user_ip: IP address of the viewer

        Raises:
            NoResultFound: If post or user doesn't exist
        """
        try:
            # Check if post exists
            post = self._post_repository.get_by_id(post_id)
            if not post:
                raise NoResultFound(f"Post with id {post_id} not found")

            # Get user
            user = self._user_repository.get_user_by_id(user_id)
            if not user:
                raise NoResultFound(f"User with id {user_id} not found")

            # Create post view
            post_view = self._post_repository.create_post_view(
                post_id=post.id,
                user_id=user.id,
                user_ip=user_ip
            )

            return True

        except Exception as e:
            self._db.rollback()
            raise e

    def get_views_by_user(self, user_id: int):
        post_with_views = self._post_repository.get_post_info_by_user(
            user_id=user_id
        )
        return post_with_views

    def post_revenue(self, post_id: int):
        total_views = self._post_repository.get_total_views(post_id=post_id)
        return self.calculate_scaling_factor(total_views)

    def scaled_revenue(self):
        scaled_views = self._post_repository.get_platform_analytics()
        return scaled_views

    def revenue_by_months(self, post_id: int):
        views_by_month = self._post_repository.get_views_by_months(
            post_id=post_id
        )
        return self.calculate_scaling_factor(views_by_month)

    def calculate_scaling_factor(self, views: Optional[dict]) -> float:
        """
            Function responsible for calculating the scaling factor
            Args:
                views

            Returns:
                Revenue scaling factor - float
        """
        scale = PostEarning.VIEW.value

        if type(views) is List[int]:
            month_views = [value * scale for key, value in views.items()]
            return month_views

        views = views.get(1)
        return views * scale

