from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    fullname: str
    email: str
    age: int


class UserCreate(User):
    hashed_password: str
    role: str
    is_active: bool = True
    created_at: datetime


class UserOut(User):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserInDB(User):
    id: int
    hashed_password: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
