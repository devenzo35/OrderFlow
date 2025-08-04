from pydantic import BaseModel
from ..models.movements import MovementType


class CategoryCreate(BaseModel):
    name: str
    type: MovementType
