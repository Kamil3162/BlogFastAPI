from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.session import Base
from ..core.enums import BlacklistReason, UserRoles
from ..core.enums import VoteType

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    votes = relationship("PostVote", back_populates="post")
    views_detail = relationship("PostView", back_populates="post")
    postCategories = relationship(
        "PostCategories",
        back_populates="post")

    @property
    def upvote(self):
        return sum(1 for vote in self.votes if vote.vote_type == VoteType.UPVOTE)
    
    @property
    def downvote(self):
        return sum(1 for vote in self.votes if vote.vote_type == VoteType.DOWNVOTE)

    @property
    def rating(self):
        return self.upvote - self.downvote

class PostVote(Base):
    __tablename__ = "post_votes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="post_votes")

    # Ensure one vote per user per post
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='uix_user_post_vote'),
    )


class PostView(Base):
    __tablename__ = "post_views"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    viewer_ip = Column(String, nullable=True, default="127.0.0.1")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)    # because user could be anonymous
    viewed_at = Column(DateTime(timezone=True), default=datetime.utcnow())

    post = relationship("Post", back_populates="views_detail")
    user = relationship("User", back_populates="post_views")

