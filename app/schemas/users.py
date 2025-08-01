from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    age: int


class UserCreate(User):
    password: str


class UserPublic(User):
    id: int
    is_active: bool
    created_at: datetime
    role: str

    class Config:
        from_attributes = True


class UserInDB(User):
    id: int
    hashed_password: str
    role: str
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class TokenRefreshRequest(BaseModel):
    refresh_token: str
