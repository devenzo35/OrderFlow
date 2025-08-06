from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CreateMovement(BaseModel):
    amount: float
    description: str | None = None
    category: str
    date: date


class UpdateMovement(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    movement_date: Optional[date] = None


class MovementPublic(BaseModel):
    id: int
    amount: float
    description: str | None = None
    category_id: int
    created_at: datetime
    date: date

    class Config:
        from_attributes = True
