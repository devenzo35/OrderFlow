from fastapi import APIRouter, Depends, HTTPException, status
from typing import Callable

from app.schemas import UserCreate, TokenRefreshRequest
from app.models import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    TOKEN_EXPIRATION_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.dependencies import get_current_user
from app.services.validators import userValidator, JWTValidator

from datetime import timedelta, timezone, datetime


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAuth2 = OAuth2PasswordBearer("/login")

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth V1"],
    responses={404: {"description": "Not found"}},
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


def role_required(required_roles: list[str]) -> Callable[[User], User]:
    def wrapper(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return wrapper


async def user_register_v1(user: UserCreate, db: AsyncSession):
    validator = userValidator(db)
    jwtValidator = JWTValidator(pwd_context)

    validator.validate_username_password(user.username, user.password)
    await validator.validate_username_email(user.username, user.email)

    user_without_password = user.model_dump(exclude={"password"})
    user_to_create = User(**user_without_password)
    user_to_create.hashed_password = jwtValidator.hash_password(user.password)

    db.add(user_to_create)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print("DETAIL:", e.orig)  # mensaje original de Postgres
        print("ARGS:", e.args)
        raise HTTPException(status_code=409, detail="Email or username already exists.")

    await db.refresh(user_to_create)
    return user_to_create


async def user_login_v1(
    form_data: OAuth2PasswordRequestForm,
    db: AsyncSession,
):
    # Here we receive username and password from the user
    user_in_db = await db.scalar(
        select(User).filter(User.username == form_data.username)
    )
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


async def refresh_token_v1(req: TokenRefreshRequest, db: AsyncSession):
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

    user = await db.scalar(select(User).filter(User.id == id))
    if not user:
        raise credentials_exception

    new_access_token = generate_access_token(data={"sub": id, "type": "access"})

    return {"access_token": new_access_token, "token_type": "bearer"}
