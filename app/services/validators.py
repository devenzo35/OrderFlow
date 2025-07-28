from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from passlib.context import CryptContext


class userValidator:
    def __init__(self, db: Session):
        self.db: Session = db

    def validate_username_email(self, username: str, email: str):
        if self.username_exists(username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Username already exists"
            )
        if self.email_exists(email):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    def validate_username_password(self, username: str, password: str):
        if username == password:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Username and passoword could not be the same",
            )

    def username_exists(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    def email_exists(self, email: str) -> bool:
        return self.db.query(User).filter(User.email == email).first() is not None


class JWTValidator:
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)
