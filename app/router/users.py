from fastapi import APIRouter, Depends
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.users import UserPublic
from typing import Annotated
from .auth import role_required

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", response_model=list[UserPublic])
async def get_all_users(
    current_user: Annotated[User, Depends(role_required(["admin"]))],
    db: Annotated[Session, Depends(get_db)],
):
    print(current_user)

    users = db.query(User).all()
    return [user for user in users]


@router.get("/{userId}", response_model=UserPublic)
async def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == userId).first()
    return user


@router.get("/inactive")
async def get_inactive_users():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]
