from pydantic import BaseModel
from typing import Optional

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



