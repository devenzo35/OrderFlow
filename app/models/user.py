from sqlalchemy.orm import Mapped, MappedColumn as Column, DeclarativeBase
from sqlalchemy import ForeignKey, Enum
from app.db.database import Base
import datetime, enum
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(primary_key=True)
    username: Mapped[str] = Column(String(30), unique=True)
    fullname: Mapped[str] = Column(String(50))
    email: Mapped[str] = Column(String(50))
    age: Mapped[str] = Column(nullable=False)
    hashed_password: Mapped[str] = Column(String(50))
    role: Mapped[str] = Column(String(30), default="user")
    is_active: Mapped[bool] = Column(default=True)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class MovementsType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"


class Movements(Base):
    __tablename__ = "movements"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    type: Mapped[MovementsType] = Column(Enum(MovementsType), nullable=False)
    amount: Mapped[float] = Column(nullable=False)
    date: Mapped[datetime.date] = Column(nullable=False)
    category_id: Mapped[int] = Column(ForeignKey("categories.id"))
    description: Mapped[str] = Column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    type: Mapped[MovementsType] = Column(Enum(MovementsType), nullable=False)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))


class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    report_type: Mapped[str] = Column(String(50))
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    file_path: Mapped[str] = Column(String(255), nullable=False)
