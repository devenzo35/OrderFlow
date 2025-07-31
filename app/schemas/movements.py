from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from ..models.movements import MovementType


class CreateMovement(BaseModel):
    amount: float
    type: MovementType
    description: str | None = None
    category_id: int
    date: date


class UpdateMovement(BaseModel):
    amount: Optional[float] = None
    type: Optional[MovementType] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    movement_date: Optional[date] = None


class MovementPublic(BaseModel):
    id: int
    amount: float
    type: MovementType
    description: str | None = None
    category_id: int
    created_at: datetime
    date: date

    class Config:
        from_attributes = True
