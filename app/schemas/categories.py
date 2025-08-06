from pydantic import BaseModel
from ..models.category import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
