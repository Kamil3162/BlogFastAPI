from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

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

    items = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo_url = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="posts")

class Comment(Base):
    __tablename__ = 'comments'


class Message(Base):
    __tablename__ = 'messages'


class Participant(Base):
    __tablename__ = 'participants'


class Room(Base):
    __tablename__ = 'rooms'


