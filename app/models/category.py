from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column, relationship
from sqlalchemy import String, Enum, ForeignKey
import enum


class CategoryType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    type: Mapped[CategoryType] = Column(Enum(CategoryType), nullable=False)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    movements = relationship("Movement", back_populates="category")
