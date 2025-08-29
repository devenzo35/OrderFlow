from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Enum, DateTime
from app.db.database import Base
import datetime
import enum
from sqlalchemy import String


class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(primary_key=True)
    username: Mapped[str] = Column(String(100), unique=True)
    fullname: Mapped[str] = Column(String(100))
    email: Mapped[str] = Column(String(100), nullable=False, unique=True)
    age: Mapped[int] = Column(nullable=False)
    hashed_password: Mapped[str] = Column(String(100), nullable=False)
    role: Mapped[RoleEnum] = Column(Enum(RoleEnum), default="user", nullable=False)
    is_active: Mapped[bool] = Column(default=True, nullable=False)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
