from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey, Date, DateTime
import datetime


class Movement(Base):
    __tablename__ = "movements"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    amount: Mapped[float] = Column(nullable=False)
    date: Mapped[datetime.date] = Column(Date, nullable=False)
    category_id: Mapped[int] = Column(ForeignKey("categories.id"))
    description: Mapped[str] = Column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now
    )
    category = relationship("Category", back_populates="movements")
