from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User
from passlib.context import CryptContext


class userValidator:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def validate_username_email(self, username: str, email: str):
        if await self.username_exists(username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Username already exists"
            )
        if await self.email_exists(email):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    def validate_username_password(self, username: str, password: str):
        if username == password:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Username and password could not be the same",
            )

    async def username_exists(self, username: str) -> bool:
        check = await self.db.scalar(select(User).filter(User.username == username))
        return check is not None

    async def email_exists(self, email: str) -> bool:
        check = await self.db.scalar(select(User).filter(User.email == email))
        return check is not None


class JWTValidator:
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)
