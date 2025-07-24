from sqlalchemy.orm import Mapped, MappedColumn as Column, DeclarativeBase
from sqlalchemy import ForeignKey, Enum
from db.database import Base
import datetime, enum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(primary_key=True)
    username: Mapped[str] = Column(string=30, unique=True)
    fullname: Mapped[str] = Column(string=50)
    email: Mapped[str] = Column(string=50)
    hashed_password: Mapped[str] = Column(string=50)
    role: Mapped[str] = Column(string=50)
    is_active: Mapped[bool] = Column(default=True)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class MovementsType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"


class Movements(Base):
    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    type: Mapped[MovementsType] = Column(
        Enum(MovementsType), nullable=False
    )  # (income, expense, investment)
    amount: Mapped[float] = Column(nullable=False)
    date: Mapped[datetime.date] = Column(nullable=False)
    category_id: Mapped[int] = Column(ForeignKey("categories.id"))
    description: Mapped[str] = Column(string=255, nullable=True)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class categories(Base):
    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(string=50, nullable=False)
    type: Mapped[MovementsType] = Column(
        Enum(MovementsType), nullable=False
    )  # (income, expense, investment)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))


class reports(Base):
    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    report_type: Mapped[str] = Column(string=50)  # (income, expense, investment)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    file_path: Mapped[str] = Column(
        string=255, nullable=False
    )  # Path to the report file
