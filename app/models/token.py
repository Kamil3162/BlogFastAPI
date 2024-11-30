from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum, Text)
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


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    jti = Column(String, unique=True, nullable=False, index=True)  # JWT ID
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    reason = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    token_type = Column(String, nullable=False)  # 'access' or 'refresh'
    user_agent = Column(Text, nullable=True)  # Browser/device info
    ip_address = Column(String, nullable=True)
