from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import Enum
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
