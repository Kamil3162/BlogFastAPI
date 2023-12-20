from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, TypeVar

T = TypeVar('T')


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        from_attributes = True


class UserSchemeOfficial(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class UserHashPassword(UserSchemeOfficial):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class RequestUserCreate(BaseModel):
    parameters: UserCreate = Field(...)


class Response:
    code: int
    status: str
    message: str
