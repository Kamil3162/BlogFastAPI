from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, func, delete

from ...schemas.category import CategoryObject
from ...models.category import PostCategory


class CategoryRepository:
    def __init__(self, db: Session):
        self._db = db
        self.model = PostCategory

    def get_by_id(self, category_id):
        category = self._db.query(self.model) \
                    .where(self.model.id == category_id)

        if not category:
            return False

        return category

    def get_post_categories(
            self,
            skip: int = 0,
            limit: int = 100,
            search: Optional[str] = None
    ) -> List[PostCategory]:
        """
        Get list of post categories with optional filtering and pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Optional search term for category name

        Returns:
            List[PostCategory]: List of post categories
        """
        query = select(self.model)

        if search:
            query = query.where(self.model.category_name.ilike(f"%{search}%"))

        query = query.offset(skip).limit(limit)
        result = self._db.execute(query)
        return result.scalars().all()

    def get_categories_with_post_count(self) -> List[dict]:
        """Get categories with their post counts"""
        query = select(
            self.model.id,
            self.model.category_name,
            func.count(self.model.post_id).label('post_count')
        ).outerjoin(
            PostCategory
        ).group_by(
            self.model.id
        )

        result = self._db.execute(query)
        return [
            {
                "id": row.id,
                "name": row.category_name,
                "post_count": row.post_count
            }
            for row in result
        ]

    def get_category_by_name(
            self,
            category_name: str
    ) -> Optional[PostCategory]:
        """Get a category by its name"""
        query = select(self.model).where(
            self.model.category_name == category_name
        )
        result = self._db.execute(query)
        return result.scalar_one_or_none()

    def create_category(
            self,
            category_name: str
    ) -> Optional[PostCategory]:
        """Create a new category"""

        category = PostCategory(category_name=category_name)

        self._db.add(category)
        self._db.commit()
        self._db.refresh(category)

        return category

    def update_category(
        self,
        category_id: int,
        category_data: CategoryObject
    ) -> PostCategory:

        category_obj = self.get_by_id(category_id)
        result = self._db.execute(category_obj)
        category = result.scalar_one_or_none()

        if not result:
            return False

        category.category_name = category_data.category_name

        self._db.commit()
        self._db.refresh(category)

        return category

    def delete_category(self, category_id: int) -> bool:
        category_obj = self.get_by_id(category_id)
        result = self._db.execute(category_obj)
        category = result.scalar_one_or_none()

        print(category)

        if not category:
            return False

        self._db.delete(category)
        self._db.commit()

        return category

    def get_all_categories(self):
        categories = self._db.query(PostCategory).all()
        # result = self._db.execute(categories)
        #
        # self._db.commit()

        return categories