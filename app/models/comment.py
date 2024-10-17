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

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    commentator_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    commentator = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")