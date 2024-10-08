from pydantic import BaseModel, EmailStr, Field
from BlogFastAPI.app.core.enums import UserRoles
from typing import Optional, TypeVar
from datetime import datetime


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

    class Config:
        from_attributes = True

class UserRoleScheme(UserSchemeOfficial):
    role: UserRoles

class UserHashPassword(UserSchemeOfficial):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class BlacklistedUserSchema(BaseModel):
    id: int
    user_id: int
    blocked_date: datetime
    reason: str

    class Config:
        from_attributes = True

class RequestUserCreate(BaseModel):
    parameters: UserCreate = Field(...)


class Response:
    code: int
    status: str
    message: str
