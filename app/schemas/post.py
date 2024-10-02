from pydantic import BaseModel
from typing import Optional
from BlogFastAPI.app.schemas.category import CategoryScheme
from BlogFastAPI.app.schemas.user import UserResponse


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