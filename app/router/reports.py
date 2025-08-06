from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Annotated
from datetime import datetime, timezone, date
from ..schemas.reports import MonthlyBalance, CategoryDistribution

# from ..models.reports import Reports
from ..models.movements import Movement
from ..models.category import Category
from ..dependencies import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


# Resumen mensual agrupado por tipo
@router.get("/month-summary", response_model=MonthlyBalance)
def get_monthly_report(
    year: Annotated[int, Query()] = datetime.now(timezone.utc).year,
    month: Annotated[int, Query()] = datetime.now(timezone.utc).month,
    db: Session = Depends(get_db),
):

    start_date = date(year, month, 1)

    if start_date.year == 12:
        end_date = date(start_date.year + 1, 1, 1)
    else:
        end_date = date(start_date.year, start_date.month + 1, 1)

    monthly_movements = (
        db.query(Category.type, func.sum(Movement.amount))
        .join(Movement, Movement.category_id == Category.id)
        .filter(Movement.date >= start_date)
        .filter(Movement.date < end_date)
        .group_by(Category.type)
    ).all()

    if not monthly_movements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movements for this month"
        )

    summary = {"month": f"{year} - {month:02d}"}

    for category, amount in monthly_movements:
        summary[category] = amount

    return summary


@router.get("/by-category", response_model=list[CategoryDistribution])
def report_by_category(
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

    # summary: list[dict[str, str | int]] = []

    # for category, amount in category_by_date:
    #     summary.append({"category": category, "total": amount})

    summary = [
        {"category": category, "total": total} for category, total in category_by_date
    ]

    return summary


# [
#   { "category_id": 1, "category_name": "Alquiler", "total": 3200.0 },
#   { "category_id": 2, "category_name": "Comida", "total": 1550.0 }
# ]

# Tendencia diaria de movimientos


@router.get("daily")
def investment_evolution(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    type: str = "income",
):
    #  [
    #   { "date": "2025-07-01", "total": 56.0 },
    #   { "date": "2025-07-02", "total": 112.0 },
    #   ...
    # ]
    return None
