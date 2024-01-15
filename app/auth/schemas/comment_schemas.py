from pydantic import BaseModel
from typing import Optional


class CommentScheme(BaseModel):
    content: str
    commentator_id: int
    post_id: int
