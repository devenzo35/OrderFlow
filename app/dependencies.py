from app.db.database import AsyncSessionLocal, asyncEngine, Base
from fastapi import Depends, HTTPException, status
from app.models.user import User
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.core.rate_limit import limiter
from app.core.config import SECRET_KEY, ALGORITHM


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


OAuth2 = OAuth2PasswordBearer("/login")


async def get_db():
    db = AsyncSessionLocal()
    async with asyncEngine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


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

    if not user.is_active:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="User is inactive, please contact with OrderFlow support service!",
        )

    return user


default_limiter: limiter = limiter.limit("10/minute")  # type: ignore
