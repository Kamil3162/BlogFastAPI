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
    category_name = Column(String)

    # posts = relationship("Post", back_populates="category")
