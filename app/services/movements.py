from fastapi import HTTPException, status
from app.models import Movement, User
from app.models.category import Category
from app.schemas import CreateMovement, UpdateMovement
from sqlalchemy.orm import Session


async def get_movements_v1(db: Session, current_user: User):
    movements = db.query(Movement).filter(Movement.user_id == current_user.id).all()

    if not movements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} has no movements yet",
        )

    return [movement for movement in movements]


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
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category does not exist"
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
