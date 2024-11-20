from pydantic import BaseModel, EmailStr
from typing import Union


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str
    exp: str

class TokenStatus(BaseModel):
    is_valid: bool


class ResetTokenSchemas(BaseModel):
    password: str
    confim_password: str