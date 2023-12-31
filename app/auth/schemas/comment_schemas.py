from pydantic import BaseModel
from typing import Optional


class Comment(BaseModel):
    content: str
    commentator_id: int
    post_id: int
