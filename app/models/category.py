from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import String, Enum, ForeignKey
from .movements import MovementType


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    type: Mapped[MovementType] = Column(Enum(MovementType), nullable=False)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
