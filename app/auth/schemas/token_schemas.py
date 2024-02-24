from pydantic import BaseModel, EmailStr
from typing import Union


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[EmailStr, None] = None

class TokenStatus(BaseModel):
    is_valid: bool