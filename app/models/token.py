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

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow)