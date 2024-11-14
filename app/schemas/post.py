from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .comment import CommentTemplate
from .category import CategoryScheme
from .user import UserResponse


class PostCreate(BaseModel):
    title: str
    content: str
    photo_url: Optional[str] = None
    owner_id: int


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    photo_url: Optional[str] = None
    owner_id: int

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostAdminInformation(BaseModel):
    title: str
    category: CategoryScheme
    owner: UserResponse
    views: int
    rating: int


class PostStats(BaseModel):
    total_views: int
    upvotes: int
    downvotes: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    photo_url: Optional[str]
    created_at: datetime
    stats: PostStats

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PostWithComments(BaseModel):
    post: PostResponse
    comments: List[CommentTemplate]

    # Configure Pydantic to work with SQLAlchemy models
    class Config:
        from_attribute = True
        arbitrary_types_allowed = True


class PostDelete(BaseModel):
    id: int
    description: str


class PostShortInfo(BaseModel):
    id: int
    title: str
    owner: UserResponse


