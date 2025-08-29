from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import bleach
from app.schemas import CategoryPublic


def validate_amount(value: Decimal):
    if value < 0:
        raise ValueError("Amount must be non-negative")
    return value


def validate_date(value: date):
    if value > date.today():
        raise ValueError("Date cannot be in the future")

    return value


def validate_description(value: str):
    if len(value) > 100:
        raise ValueError("Description must be 100 characters or fewer")
    return bleach.clean(value, strip=True)


class BaseMovement(BaseModel):
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    description: str | None = None
    category: str
    date: date

    @field_validator("amount")
    def validate_amount(cls, value: Decimal):
        return validate_amount(value)

    @field_validator("date")
    def validate_date(cls, value: datetime):
        return validate_date(value)

    @field_validator("description")
    def validate_description(cls, value: str):
        return validate_description(value)


class CreateMovement(BaseMovement):
    pass


class UpdateMovement(BaseModel):
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    category: Optional[str] = None
    movement_date: Optional[date] = None

    @field_validator("amount")
    def validate_amount(cls, value: Decimal):
        return validate_amount(value)

    @field_validator("movement_date")
    def validate_date(cls, value: datetime):
        return validate_date(value)

    @field_validator("description")
    def validate_description(cls, value: str):
        return validate_description(value)


# TODO: add category info to movement public schema


class MovementPublic(BaseModel):
    id: int
    amount: Decimal
    description: str
    created_at: datetime
    category: CategoryPublic

    class Config:
        from_attributes = True
