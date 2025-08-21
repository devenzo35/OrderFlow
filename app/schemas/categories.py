from pydantic import BaseModel
from ..models.category import CategoryType
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryPublic(BaseModel):
    id: int
    name: str
    type: CategoryType


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
