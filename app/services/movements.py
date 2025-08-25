from fastapi import HTTPException, status
from app.models import Movement, User
from app.models.category import Category
from app.schemas import CreateMovement, UpdateMovement
from sqlalchemy.orm import Session
import math


async def get_movements_v1(
    db: Session, current_user: User, page_size: int = 10, page: int = 1
):
    offset = (page - 1) * page_size

    db_movements = db.query(Movement).filter(Movement.user_id == current_user.id)

    total_movements = db_movements.count()

    if total_movements == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} has no movements yet",
        )

    filtered_movements = db_movements.limit(page_size).offset(offset).all()
    total_pages = math.ceil(float(total_movements / page_size))

    previous = (
        f"api/v1/movements?page={page - 1}&page_size={page_size}" if page > 1 else None
    )
    next = (
        f"api/v1/movements?page={page + 1}&page_size={page_size}"
        if page < total_pages
        else None
    )

    return {
        "data": [movement for movement in filtered_movements],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total": total_movements,
            "next": next,
            "previous": previous,
        },
    }  # type: ignore


async def get_movement_v1(
    movement_id: int,
    db: Session,
    current_user: User,
):
    movement = (
        db.query(Movement)
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
        .first()
    )

    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movement with id: {movement_id} does not exist for user {current_user.username}",
        )

    return movement


async def create_movement_v1(
    movement: CreateMovement,
    db: Session,
    current_user: User,
):
    # Business rule: Amount must be positive to ensure only valid income entries.
    if movement.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than zero",
        )

    category_db = (
        (db.query(Category).filter(Category.name == movement.category))
        .filter(Category.user_id == current_user.id)
        .first()
    )

    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    new_movement = Movement(
        **movement.model_dump(exclude={"category"}),
        user_id=current_user.id,
        category_id=category_db.id,
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


async def update_movement_v1(
    movement_id: int,
    movement_update: UpdateMovement,
    db: Session,
    current_user: User,
):
    movement_to_update = (
        db.query(Movement)
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
    ).first()
    if not movement_to_update:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Movement does not exist")

    movement_fields = movement_update.model_dump(exclude_unset=True)

    forbidden_fields = ["created_at", "id", "user_id"]

    for field in movement_fields:
        if field in forbidden_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden action",
            )

    for field, value in movement_fields.items():
        setattr(movement_to_update, field, value)

    db.commit()
    db.refresh(movement_to_update)

    return movement_to_update


async def delete_movement_v1(
    movement_id: int,
    db: Session,
    current_user: User,
):
    movement = (
        db.query(Movement)
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
        .first()
    )

    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movement does not exist"
        )

    db.delete(movement)
    db.commit()

    return movement
