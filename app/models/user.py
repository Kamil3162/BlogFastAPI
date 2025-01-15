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
    role = Column(Enum(UserRoles), default=UserRoles.BLOGGER)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="commentator")
    blacklisted_users = relationship("BlacklistedUser",
                                     back_populates="user",
                                     uselist=False)
    post_votes = relationship("PostVote", back_populates="user")
    post_views = relationship("PostView", back_populates="user")
    views_detail = relationship("PostView", back_populates="user")

    def __str__(self):
        return f"User(id={self.id}, email='{self.email}', first_name='{self.first_name}', " \
               f"last_name='{self.last_name}', is_active={self.is_active}, " \
               f"is_verified={self.is_verified}, created_at={self.created_at}, " \
               f"updated_at={self.updated_at})"

    @property
    def user_scaled_information(self):
        return f"{self.first_name} {self.last_name}"


class BlacklistedUser(Base):
    __tablename__ = "blacklisted_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blocked_data = Column(DateTime)
    reason = Column(Enum(BlacklistReason))

    user = relationship("User", back_populates="blacklisted_users")