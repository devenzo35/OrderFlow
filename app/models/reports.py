from ..db.database import Base
from sqlalchemy.orm import Mapped, mapped_column as Column
from sqlalchemy import ForeignKey, String, Enum
import datetime
import enum


class ReportTypes(str, enum.Enum):
    monthly_balance = "monthly_balance"
    category_distribution = "category_distribution"
    investment_evolution = "investment_evolution"
    custom = "custom"


class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = Column(primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    report_type: Mapped[ReportTypes] = Column(Enum(ReportTypes), nullable=False)
    created_at: Mapped[datetime.datetime] = Column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    file_path: Mapped[str] = Column(String(255), nullable=False)
