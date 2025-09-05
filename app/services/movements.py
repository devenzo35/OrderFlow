from fastapi import HTTPException, status
from app.models import Movement, User
from app.models.category import Category
from app.schemas import CreateMovement, UpdateMovement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
import math
from app.core.app_logging import logger


async def get_movements_v1(
    db: AsyncSession, current_user: User, page_size: int = 10, page: int = 1
) -> dict[str, list[Movement] | dict[str, int | str | None]]:
    offset = (page - 1) * page_size

    total_movements = await db.scalar(
        select(func.count(Movement.id)).filter(Movement.user_id == current_user.id)
    )

    if not total_movements or total_movements == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} has no movements yet",
        )

    filtered_movements = await db.scalars(
        select(Movement)
        .filter(Movement.user_id == current_user.id)
        .limit(page_size)
        .offset(offset)
    )

    if not filtered_movements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} has no movements yet",
        )

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
    }


async def get_movement_v1(
    movement_id: int,
    db: AsyncSession,
    current_user: User,
):
    movement = await db.scalar(
        select(Movement)
        .options(selectinload(Movement.category))
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
    )

    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movement with id: {movement_id} does not exist for user {current_user.username}",
        )

    return movement


async def create_movement_v1(
    movement: CreateMovement,
    db: AsyncSession,
    current_user: User,
):
    # Business rule: Amount must be positive to ensure only valid income entries.
    if movement.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than zero",
        )

    category_db = await db.scalar(
        select(Category)
        .filter(Category.name == movement.category.lower())
        .filter(Category.user_id == current_user.id)
    )

    if not category_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    exists = await db.scalar(
        select(Movement)
        .filter(Movement.description == movement.description)
        .filter(Movement.category_id == category_db.id)
        .filter(Movement.user_id == current_user.id)
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Movement already exists"
        )

    new_movement = Movement(
        **movement.model_dump(exclude={"category"}),
        user_id=current_user.id,
        category_id=category_db.id,
    )

    db.add(new_movement)

    try:
        await db.commit()
        await db.refresh(new_movement)
        logger.info(
            "User %s created movement: %s", new_movement.user_id, new_movement.id
        )
        result = await db.scalar(
            select(Movement)
            .options(selectinload(Movement.category))
            .filter(Movement.id == new_movement.id)
        )
        return result
    except Exception as e:
        logger.error(
            "Error creating movement",
            extra={"user_id": new_movement.user_id, "error": str(e)},
        )


# TODO: Work in update movement and handle movement category update
async def update_movement_v1(
    movement_id: int,
    movement_data: UpdateMovement,
    db: AsyncSession,
    current_user: User,
):
    movement_to_update = await db.scalar(
        select(Movement)
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
    )
    if not movement_to_update:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Movement does not exist")

    movement_fields = movement_data.model_dump(exclude_unset=True, exclude={"category"})

    if movement_data.category:
        category_db = await db.scalar(
            select(Category)
            .filter(Category.name == movement_data.category)
            .filter(Category.user_id == current_user.id)
        )
        if not category_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist or does not belong to the user",
            )

        movement_fields["category_id"] = category_db.id

    forbidden_fields = ["created_at", "id", "user_id"]

    for field in movement_fields:
        if field in forbidden_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden action",
            )

    for field, value in movement_fields.items():
        setattr(movement_to_update, field, value)

    await db.commit()
    await db.refresh(movement_to_update)

    return movement_to_update


async def delete_movement_v1(
    movement_id: int,
    db: AsyncSession,
    current_user: User,
):
    movement = await db.scalar(
        select(Movement)
        .filter(Movement.id == movement_id)
        .filter(Movement.user_id == current_user.id)
    )

    if not movement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movement does not exist"
        )

    await db.delete(movement)
    await db.commit()

    return movement
