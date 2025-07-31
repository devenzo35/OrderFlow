from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey, Enum, Date, DateTime
import datetime, enum


class MovementType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"


class Movement(Base):
    __tablename__ = "movements"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    type: Mapped[MovementType] = Column(Enum(MovementType), nullable=False)
    amount: Mapped[float] = Column(nullable=False)
    date: Mapped[datetime.date] = Column(Date, nullable=False)
    category_id: Mapped[int] = Column(ForeignKey("categories.id"))
    description: Mapped[str] = Column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now
    )
