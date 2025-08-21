from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas import UserPublic, UserCreate, TokenRefreshRequest
from app.models import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.dependencies import get_db, get_current_user
from app.services.user_auth import user_login_v1, user_register_v1, refresh_token_v1


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
async def user_register(user: UserCreate, db: Session = Depends(get_db)):
    return await user_register_v1(user, db)


@router.post("/login", status_code=200)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    return await user_login_v1(form_data, db)


@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.post("/token/refresh")
async def refresh_token(req: TokenRefreshRequest, db: Session = Depends(get_db)):
    return await refresh_token_v1(req, db)
