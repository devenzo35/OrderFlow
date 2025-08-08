from fastapi import APIRouter, status, Depends, HTTPException
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.category import Category
from ..models.movements import Movement
from ..schemas.movements import CreateMovement, MovementPublic, UpdateMovement
from .auth import get_current_user

router = APIRouter(
    prefix="/movements",
    tags=["movements"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


@router.get("/all", response_model=list[MovementPublic])
def get_my_movements(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    movements = db.query(Movement).filter(Movement.user_id == current_user.id).all()

    if not movements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {current_user.username} has no movements yet",
        )

    return [movement for movement in movements]


@router.post("/create", response_model=MovementPublic, status_code=201)
async def create_movement(
    movement: CreateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.get("/{movement_id}", response_model=MovementPublic)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.patch("/update/{movement_id}", status_code=200)  # response_model=MovementPublic
async def update_movement(
    movement_id: int,
    movement_update: UpdateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.delete("/{movement_id}", response_model=MovementPublic)
async def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
