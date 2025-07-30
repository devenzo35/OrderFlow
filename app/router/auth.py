from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Callable
from app.schemas.users import UserPublic, UserCreate, TokenRefreshRequest
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
REFRESH_TOKEN_EXPIRE_DAYS = 7

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


def generate_refresh_token(data: dict[str, str | datetime]):
    to_encode = data.copy()

    print(to_encode)
    token_expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": token_expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(OAuth2)], db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type:ignore
        id: int = payload.get("sub")

        if not id:
            raise credentials_exception

    except InvalidTokenError:

        raise credentials_exception

    user = db.query(User).filter(User.id == id).first()

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

    return currentUser


def role_required(required_roles: list[str]) -> Callable[[User], User]:
    def wrapper(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return wrapper


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

    access_token = generate_access_token(
        data={
            "sub": str(user_in_db.id),
            "role": str(user_in_db.role.value),
            "type": "access",
        }
    )
    refresh_token = generate_refresh_token(
        data={"sub": str(user_in_db.id), "role": str(user_in_db.role.value)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/token/refresh")
def refresh_token(req: TokenRefreshRequest, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(  # type:ignore
            req.refresh_token, SECRET_KEY, algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail="Invalid token type"
            )
        id = payload.get("sub")
        if not id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise credentials_exception

    new_access_token = generate_access_token(data={"sub": id, "type": "access"})

    return {"access_token": new_access_token, "token_type": "bearer"}
