from sqlalchemy.orm import Session
from base import BaseRepository
from ...models.category import PostCategory

class CategoryRepository(BaseRepository):
    def __init__(self, PostCategory, db: Session):
        super().__init__(PostCategory, db)

