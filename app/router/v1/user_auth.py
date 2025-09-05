from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Annotated
from app.schemas import UserPublic, UserCreate, TokenRefreshRequest
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.dependencies import get_db, get_current_user, default_limiter  # type: ignore
from app.services.user_auth import user_login_v1, user_register_v1, refresh_token_v1
from app.core.rate_limit import limiter

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


@router.post("/register", status_code=201, response_model=UserPublic)
@default_limiter  # type: ignore
async def user_register(
    request: Request, user: UserCreate, db: AsyncSession = Depends(get_db)
):
    return await user_register_v1(user, db)


@router.post("/login", status_code=200)
@limiter.limit("5/minute")  # type: ignore
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    return await user_login_v1(request, form_data, db)


@router.get("/me", response_model=UserPublic)
@default_limiter  # type: ignore
async def read_users_me(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.post("/token/refresh")
@default_limiter  # type: ignore
async def refresh_token(
    request: Request,
    req: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    return await refresh_token_v1(req, db)
