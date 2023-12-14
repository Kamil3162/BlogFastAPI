from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    is_active: bool = None