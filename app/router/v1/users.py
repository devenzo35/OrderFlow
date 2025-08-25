from fastapi import APIRouter, Depends
from ...dependencies import get_db
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter
from fastapi import Request
from app.models import User
from app.schemas import UserPublic
from typing import Annotated
from app.services.user_auth import role_required
from app.services.users import get_users_v1, get_user_v1

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users V1"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[UserPublic])
@limiter.limit("15/minute")  # type: ignore
async def get_all_users(
    request: Request,
    current_user: Annotated[User, Depends(role_required(["admin"]))],
    db: Annotated[Session, Depends(get_db)],
):
    return await get_users_v1(db)


@router.get("/{user_id}", response_model=UserPublic)
@limiter.limit("20/minute")  # type: ignore
async def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    return await get_user_v1(user_id, db)


@router.get("/inactive")
async def get_inactive_users():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]
