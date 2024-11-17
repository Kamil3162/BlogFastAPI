from sqlalchemy import exc, desc
from sqlalchemy.orm import Session

from ...models.post import Post
from ...models.category import PostCategory
from ...schemas.post import PostCreate


class PostRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_by_id(self, db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        return post

    def get_by_title(self, db: Session, title: str) -> Post:
        post = db.query(Post).filter(Post.title.ilike(f'%{title}%')).first()
        return post

    def get_by_category(self, db: Session, category_name):
        posts = db.query(Post) \
            .join(Post.categories) \
            .join(PostCategory) \
            .filter(PostCategory.category_name == category_name).all()
        return posts

    def create(self, db: Session, post_data: PostCreate, owner_id: int):
        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            photo_url=str(
                post_data.photo_url) if post_data.photo_url else None,
            owner_id=owner_id
        )
        db.add(db_post)
        db.commit()

        return db_post

    def update(self, post_instance, post_data: PostCreate, db: Session):
        for key, value in post_data.model_fields_set:
            setattr(post_instance, key, value)
        db.commit()
        db.refresh(post_instance)
        return post_instance

    def get_posts(self, db: Session):
        posts = db.query(Post).all()
        return posts

    def get_posts_range(self, db: Session, skip: int = 0, limit: int = 10):
        posts = db.query(Post).offset(skip).limit(limit).all()
        return posts

    def get_newest_post(self, db: Session):
        newest_post = db.query(Post).order_by(desc(Post.created_at).first())
        return newest_post

    def delete_post(self, db:Session, post_id):
        result = self._db.query(Post).filter(Post.id == post_id).delete()
        return bool(result)
