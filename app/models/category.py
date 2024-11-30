from datetime import datetime

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

from ..db.session import Base
from ..core.enums import BlacklistReason, UserRoles

class PostCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)

    post_categories = relationship(
        "PostCategories",
        back_populates="category"
    )

class PostCategories(Base):
    __tablename__ = "posts_categories"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    post = relationship("Post", back_populates="post_categories")
    category = relationship(
        "PostCategory",
        back_populates="post_categories")
