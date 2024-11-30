from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.post import Post
from ...models.category import PostCategory, PostCategories

class PostsCategoriesRepository:
    def __init__(self, db: Session):
        self._db = db

    def filter_assigned_categories_to_post(
        self,
        post: Post,
        category: PostCategory
    ):
        post_category = self._db.query(PostCategories).where(
            PostCategories.post_id == post.id,
            PostCategories.category_id == category.id
        ).first()

        return post_category

    def assign_category_to_post(self, post: Post, category: PostCategory):
        """
            Create a new post-category relationship.
        """
        post_category = PostCategories(
            post_id=post.id,
            category_id=category.id
        )

        self._db.add(post_category)
        self._db.commit()
        return post_category

    def get_assigned_category_to_post(self, post: Post):
        query = self._db.query(PostCategories).join(PostCategory).where(
            PostCategories.post_id == post.id
        )

        result = self._db.execute(query)
        return result.scalars().all()

    def update_assigned_category_for_post(
        self,
        post: Post,
        category: PostCategory
    ):
        post_category = self.filter_assigned_categories_to_post(post, category)

        if not post_category:
            return False

        post_category.post_id = post.id
        post_category.category_id = category.id

        self._db.refresh(post_category)
        self._db.commit()
        return True

    def remove_category_from_post(self, post: Post, category: PostCategory):
        post_category = self._db.query(PostCategories).where(
            PostCategories.post_id == post.id,
            PostCategories.category_id == category.id
        ).first()

        if not post_category:
            return False

        self._db.delete(post_category)
        self._db.commit()
        return True