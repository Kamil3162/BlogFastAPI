from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CommentScheme(BaseModel):
    content: str
    commentator_id: int
    post_id: int


class CommentUpdate(BaseModel):
    content: str
    comment_id: int


class CommentTemplate(BaseModel):
    id: int
    content: str
    commentator_id: int
    post_id: int
    created_at: datetime

class CommentBaseScheme(BaseModel):
    id: int
    post_id: int
    commentator_id: int