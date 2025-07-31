from fastapi import APIRouter, status, Depends, HTTPException
from ..dependencies import get_db
from sqlalchemy.orm import Session
from ..models.user import User
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
        return [{"message": "No financial movements found for this user."}]

    return [movement for movement in movements]


@router.post("/create/", response_model=MovementPublic, status_code=201)
def create_movement(
    movement: CreateMovement,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_movement = Movement(
        **movement.model_dump(exclude={"type"}),
        user_id=current_user.id,
        type=movement.type.INCOME
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


@router.patch("/update/{movement_id}", status_code=200)  # response_model=MovementPublic
def update_movement(
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

    for field, value in movement_fields.items():
        setattr(movement_to_update, field, value)

    db.commit()
    db.refresh(movement_to_update)

    return movement_to_update
