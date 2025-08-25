from typing import Annotated
from fastapi import APIRouter, Query, status, Depends
from ...dependencies import get_db, get_current_user, default_limiter  # type: ignore
from fastapi import Request
from sqlalchemy.orm import Session

# from ..models.user import User
# from ..models.category import Category
# from ..models.movements import Movement

from app.models import User
from app.services.movements import (
    get_movements_v1,
    get_movement_v1,
    create_movement_v1,
    update_movement_v1,
    delete_movement_v1,
)

from app.schemas import CreateMovement, MovementPublic, UpdateMovement


router = APIRouter(
    prefix="/api/v1/movements",
    tags=["Movements V1"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


@router.get("/")
@default_limiter  # type: ignore
async def get_movements(
    request: Request,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=1, le=100)] = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_movements_v1(db, current_user, page_size, page)


@router.post("/", response_model=MovementPublic, status_code=201)
@default_limiter  # type: ignore
async def create_movement(
    request: Request,
    movement: CreateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_movement_v1(movement, db, current_user)


@router.get("/{movement_id}", response_model=MovementPublic)
@default_limiter  # type: ignore
async def get_movement(
    request: Request,
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_movement_v1(movement_id, db, current_user)


@router.patch("/{movement_id}", status_code=200)  # response_model=MovementPublic
@default_limiter  # type: ignore
async def update_movement(
    request: Request,
    movement_id: int,
    movement_update: UpdateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_movement_v1(movement_id, movement_update, db, current_user)


@router.delete("/{movement_id}", response_model=MovementPublic)
@default_limiter  # type: ignore
async def delete_movement(
    request: Request,
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_movement_v1(movement_id, db, current_user)
