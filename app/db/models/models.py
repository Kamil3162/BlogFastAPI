import enum
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
from ..database import Base
from .enums import BlacklistReason, UserRoles
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
    photo_url = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id'))
    views = Column(Integer, default=0)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    sections = relationship("Section", back_populates="post")

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




