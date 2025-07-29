from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas.users import UserPublic, UserCreate, JwtToken
from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError

from ..dependencies import get_db
from ..services.validators import userValidator, JWTValidator

from dotenv import load_dotenv
import os
from datetime import timedelta, timezone, datetime

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRATION_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAuth2 = OAuth2PasswordBearer("/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/register", status_code=201, response_model=UserPublic)
async def user_register(user: UserCreate, db: Session = Depends(get_db)):

    validator = userValidator(db)
    jwtValidator = JWTValidator(pwd_context)

    validator.validate_username_password(user.username, user.password)
    validator.validate_username_email(user.username, user.email)

    user_without_password = user.model_dump(exclude={"password"})
    user_to_create = User(**user_without_password)
    user_to_create.hashed_password = jwtValidator.hash_password(user.password)

    db.add(user_to_create)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists.")

    db.refresh(user_to_create)
    return user_to_create


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_access_token(data: dict[str, str | datetime]):
    to_encode = data.copy()

    token_expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRATION_MINUTES
    )
    to_encode.update({"exp": token_expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore

    return encoded_jwt


@router.post("/login", status_code=200)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):

    # Here we receive username and password from the user
    user_in_db = db.query(User).filter(User.username == form_data.username).first()
    if not user_in_db:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="invalid username or password"
        )

    if not verify_password(form_data.password, user_in_db.hashed_password):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="invalid username or password"
        )

    token = generate_access_token(data={"sub": user_in_db.username})

    return token


async def get_current_user(
    token: Annotated[str, Depends(OAuth2)], db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type:ignore
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise credentials_exception

    return user


async def get_current_active_user(
    currentUser: Annotated[User, Depends(get_current_user)],
):
    if not currentUser.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="User is inactive, please contact with OrderFlow support service!",
        )


@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
