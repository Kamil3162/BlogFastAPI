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


class PostMark(Base):
    __tablename__ = "post_mark"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="post_mark")