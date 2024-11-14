from datetime import datetime

from sqlalchemy import (
    Boolean,
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
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey('users.id'))

    categories = relationship("PostCategories", back_populates="post")
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    sections = relationship("Section", back_populates="post")
    votes = relationship("PostVote", back_populates="post")

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
    post_id = Column(Integer, ForeignKey("posts.id"))
    viewer_ip = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    viewed_at = Column(DateTime(timezone=True), default=datetime.utcnow())

    post = relationship("Post", back_populates="views_detail")



'''
    from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from BlogFastAPI.app.db.database import Base
from BlogFastAPI.app.core.enums import BlacklistReason, UserRoles
CONSTANT = 32

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    role = Column(Enum(UserRoles), default=UserRoles.BLOGGER)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="commentator")
    blacklisted_users = relationship("BlacklistedUser",
                                     back_populates="user",
                                     uselist=False)

    def __str__(self):
        return f"User(id={self.id}, email='{self.email}', first_name='{self.first_name}', " \
               f"last_name='{self.last_name}', is_active={self.is_active}, " \
               f"is_verified={self.is_verified}, created_at={self.created_at}, " \
               f"updated_at={self.updated_at})"

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo_url = Column(String, nullable=True)
    views = Column(Integer, default=0)
    mark = Column(Integer, default=1)

    owner_id = Column(Integer, ForeignKey('users.id'))

    categories = relationship("PostCategories", back_populates="post")
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    sections = relationship("Section", back_populates="post")
    post_mark = relationship("PostMark", back_populates="post")

class PostCategories(Base):
    __tablename__ = "posts_categories"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    post = relationship("Post", back_populates="categories")
    category = relationship("PostCategory", back_populates="posts")

class Section(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo_url = Column(String)

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="sections")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    commentator_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    commentator = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# Define the revoked tokens model
class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow)

class BlacklistedUser(Base):
    __tablename__ = "blacklisted_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blocked_data = Column(DateTime)
    reason = Column(Enum(BlacklistReason))

    user = relationship("User", back_populates="blacklisted_users")

class PostMark(Base):
    __tablename__ = "post_mark"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="post_mark")

# class Message(Base):
#     __tablename__ = 'messages'
#
#
# class Participant(Base):
#     __tablename__ = 'participants'
#
#
# class Room(Base):
#     __tablename__ = 'rooms'

'''