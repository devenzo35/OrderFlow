from fastapi import APIRouter, status, Depends, HTTPException
from ...dependencies import get_db, get_current_user
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


@router.get("/", response_model=list[MovementPublic])
async def get_movements(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await get_movements_v1(db, current_user)


@router.post("/", response_model=MovementPublic, status_code=201)
async def create_movement(
    movement: CreateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_movement_v1(movement, db, current_user)


@router.get("/{movement_id}", response_model=MovementPublic)
async def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_movement_v1(movement_id, db, current_user)

    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movement with id: {movement_id} does not exist for user {current_user.username}",
        )

    return movement


@router.patch("/{movement_id}", status_code=200)  # response_model=MovementPublic
async def update_movement(
    movement_id: int,
    movement_update: UpdateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await update_movement_v1(movement_id, movement_update, db, current_user)


@router.delete("/{movement_id}", response_model=MovementPublic)
async def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_movement_v1(movement_id, db, current_user)
