from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re


def validate_username_value(value: str):
    if len(value) < 3:
        raise ValueError("Username must be at least 4 characters long")
    if len(value) > 30:
        raise ValueError("Username too long")
    if not re.fullmatch("^(?![0-9]+$)[A-Za-z0-9]+$", value):
        raise ValueError("Invalid username format")
    return value.lower()


class User(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    age: int

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        return validate_username_value(value)

    @field_validator("fullname")
    def validate_fullname(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("fullname must have at least 4 characters and two words")
        if len(value) > 30:
            raise ValueError("Username too long")
        if len(value.split()) < 2:
            raise ValueError("fullname must have at least two words")
        if not re.fullmatch(r"^[A-Za-z]+([ '-][A-Za-z]+)*$", value):
            raise ValueError("Invalid fullname format")
        return value.lower()

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if len(value) < 0:
            raise ValueError("Email address is required")
        if len(value) > 30:
            raise ValueError("Email too long")
        if not re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", value):
            raise ValueError("Invalid email format")
        return value.lower()


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

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        return validate_username_value(value)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(value) > 100:
            raise ValueError("Password is too long")
        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$", value
        ):
            raise ValueError(
                "Password must contain uppercase, lowercase, digit, and special character"
            )
        return value

    class Config:
        from_attributes = True


class TokenRefreshRequest(BaseModel):
    refresh_token: str
