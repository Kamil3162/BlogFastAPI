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
from ..db.session import Base
from ..core.enums import BlacklistReason, UserRoles

class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    photo_url = Column(String)

    post_id = Column(Integer, ForeignKey('posts.id'))

    post = relationship("Post", back_populates="sections")



