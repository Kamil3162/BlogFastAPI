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

class PostMark(Base):
    __tablename__ = "post_mark"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="post_mark")