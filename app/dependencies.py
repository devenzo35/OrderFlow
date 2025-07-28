from typing import Annotated

from fastapi import Header, HTTPException, status, Depends
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_token_header(x_token: Annotated[str, Depends(Header())]):
    if not x_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Token is invalid"
        )


async def get_query_token(token: str):
    if token != "query":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
