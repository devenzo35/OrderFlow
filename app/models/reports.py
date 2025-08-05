from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import ForeignKey, String
import datetime


class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    report_type: Mapped[str] = Column(String(100))
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    file_path: Mapped[str] = Column(String(255), nullable=False)
