from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.category import Category
from ..models.movements import Movement
from typing import Annotated
from ..dependencies import get_db
from fastapi.responses import StreamingResponse
from io import StringIO
import csv
from datetime import date

router = APIRouter(
    prefix="/export",
    tags=["export"],
    responses={status.HTTP_400_BAD_REQUEST: {"message": "URL Not Found"}},
)


@router.get("/export/by-category/csv")
def export_category_report(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    db: Session = Depends(get_db),
):
    category_by_date = (
        db.query(Category.name, func.sum(Movement.amount))
        .join(Category, Category.id == Movement.category_id)
        .filter(Movement.date >= start_date)
        .filter(Movement.date <= end_date)
        .group_by(Category.name)
    ).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Category", "Total"])

    for category, total in category_by_date:
        writer.writerow([category, total])

    output.seek(0)

    file_path = f"report_by_category_{start_date}-{end_date}.csv"
    return None
