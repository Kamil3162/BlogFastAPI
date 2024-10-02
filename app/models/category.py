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
from BlogFastAPI.app.db.session import Base
from BlogFastAPI.app.core.enums import BlacklistReason, UserRoles
class PostCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)

    posts = relationship("PostCategories", back_populates="category")
