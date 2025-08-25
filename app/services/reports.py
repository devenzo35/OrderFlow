from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Movement, Category
from datetime import date


async def monthly_report_v1(
    year: int,
    month: int,
    db: Session,
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


async def by_category_report_v1(
    start_month: date,
    end_month: date,
    db: Session,
):
    category_by_date = (
        db.query(Category.name, func.sum(Movement.amount))
        .join(Category, Category.id == Movement.category_id)
        .filter(Movement.date >= start_month)
        .filter(Movement.date <= end_month)
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


async def investment_evolution_v1(
    start_date: date,
    end_date: date,
    type: str = "income",
):
    #  [
    #   { "date": "2025-07-01", "total": 56.0 },
    #   { "date": "2025-07-02", "total": 112.0 },
    #   ...
    # ]
    return None
