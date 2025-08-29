from pydantic import BaseModel, field_validator
from ..models.category import CategoryType
from typing import Optional


def validate_name(value: str):
    if len(value) < 0:
        raise ValueError("Field name is required")
    if len(value) > 50:
        raise ValueError("Name is too long")
    return value.lower()


class BaseCategory(BaseModel):
    name: str
    type: CategoryType

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        return validate_name(value)


class CategoryCreate(BaseCategory):
    pass


class CategoryPublic(BaseCategory):
    id: int


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        return validate_name(value)
