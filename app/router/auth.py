from fastapi import APIRouter, Depends

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from app.schemas.users import UserPublic, UserCreate
from app.models.user import User
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os

load_dotenv()


ALGORITH = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register", response_model=UserPublic)
async def user_register(user: UserCreate, db: Session = Depends(get_db)):

    user_without_password = user.model_dump(exclude={"password"})
    user_to_create = User(**user_without_password)
    user_to_create.hashed_password = hash_password(user.password)
    user_db = db.add(user_to_create)

    db.commit()
    db.refresh(user_db)
    return user_to_create
