from sqlalchemy.orm import Mapped, mapped_column as Column, relationship
from sqlalchemy import ForeignKey, Enum
from app.db.database import Base
import datetime, enum
from sqlalchemy import String


class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(primary_key=True)
    username: Mapped[str] = Column(String(100), unique=True)
    fullname: Mapped[str] = Column(String(100))
    email: Mapped[str] = Column(String(100))
    age: Mapped[str] = Column(nullable=False)
    hashed_password: Mapped[str] = Column(String(100))
    role: Mapped[RoleEnum] = Column(Enum(RoleEnum), default="user")
    is_active: Mapped[bool] = Column(default=True)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class MovementsType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(primary_key=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    type: Mapped[MovementsType] = Column(Enum(MovementsType), nullable=False)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))


class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    report_type: Mapped[str] = Column(String(100))
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    file_path: Mapped[str] = Column(String(255), nullable=False)
