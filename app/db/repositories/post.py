from sqlalchemy import exc, desc, select
from sqlalchemy.orm import Session

from ...models.post import Post, PostVote, PostView
from ...models.category import PostCategory
from ...schemas.post import PostCreate, PostUpdate
from ...core.enums import VoteType

class PostRepository:
    def __init__(self, db: Session):
        self._db = db
        self._model = Post

    def get_by_id(self, db: Session, post_id: int):
        stmt = select(self._model).where(self._model.id == post_id)
        result = self._db.execute(stmt)
        modern_way = result.scalar_one_or_none()

        return modern_way

    def get_by_title(self, db: Session, title: str) -> Post:
        post = db.query(Post).filter(Post.title.ilike(f'%{title}%')).first()
        return post

    def get_by_category(self, db: Session, category_name):
        posts = db.query(Post) \
            .join(Post.categories) \
            .join(PostCategory) \
            .filter(PostCategory.category_name == category_name).all()
        return posts

    def create(self, post_data: PostCreate):
        print("create function")

        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            photo_url=post_data.photo_url,
            owner_id=post_data.owner_id
        )

        self._db.add(db_post)
        self._db.commit()

        return db_post

    def update(self, post_instance: Post, post_data: PostUpdate):
        """
            Update model instance with new data.

            Args:
                post_instance: Post class object
                post_data: Schema used to update

            Returns:
                Updated instance of None if not found
        """

        update_data = post_data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in update_data.items():
            if hasattr(post_instance, key):
                setattr(post_instance, key, value)

        self._db.add(post_instance)
        self._db.commit()
        self._db.refresh(post_instance)

        return post_instance

    def get_posts(self, db: Session):
        posts = db.query(Post).all()
        return posts

    def get_posts_range(self, db: Session, skip: int = 0, limit: int = 10):
        posts = db.query(Post).offset(skip).limit(limit).all()
        return posts

    def get_newest_post(self, db: Session):
        newest_post = db.query(self._model).order_by(
            desc(self._model.created_at).first()
        )
        return newest_post

    def delete_post(self, post_id):
        result = self._db.query(Post).filter(Post.id == post_id).delete()

        return bool(result)

    # functions responsible for get vote instances
    def upvote_create(self, user_id, post_id, vote_type: VoteType):
        post_vote = PostVote(
            post_id=post_id,
            user_id=user_id,
            vote_type=vote_type,
        )

        self._db.add(post_vote)
        self._db.commit()

    def upvote_delete(self, post_id, user_id):
        post_vote = self._db.query(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        ).one()

        self._db.delete(post_vote)
        self._db.commit()

    def upvote_update(self, post_id, user_id, vote_type: VoteType):
        post_vote = self._db.query(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        ).one()

        post_vote.vote_type = vote_type

        self._db.refresh(post_vote)
        self._db.commit()

        return post_vote

    def get_vote_instance(self, user_id, post_id):
        post_vote = self._db.query(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        )

        return post_vote

    # functions responsible for operate on views
    def create_post_view(
        self,
        post_id: int,
        user_id: int,
        user_ip: str = "127.0.0.1"
    ):
        post_view = PostView(
            post_id=post_id,
            user_id=user_id,
            viewer_ip=user_ip
        )

        self._db.add(post_view)
        self._db.commit()

