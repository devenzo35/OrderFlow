from fastapi import APIRouter, Depends, status, Query
from typing import Annotated
from datetime import datetime, timezone, date
from app.schemas import MonthlyBalance, CategoryDistribution
from app.services.reports import (
    by_category_report_v1,
    investment_evolution_v1,
    monthly_report_v1,
)

from ...dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports V1"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


# Resumen mensual agrupado por tipo
@router.get("/month-summary", response_model=MonthlyBalance)
async def get_monthly_report(
    year: Annotated[int, Query()] = datetime.now(timezone.utc).year,
    month: Annotated[int, Query()] = datetime.now(timezone.utc).month,
    db: Session = Depends(get_db),
):
    return await monthly_report_v1(year, month, db)


@router.get("/by-category", response_model=list[CategoryDistribution])
async def by_category_report(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    db: Session = Depends(get_db),
):
    return await by_category_report_v1(start_date, end_date, db)


# [
#   { "category_id": 1, "category_name": "Alquiler", "total": 3200.0 },
#   { "category_id": 2, "category_name": "Comida", "total": 1550.0 }
# ]

# Tendencia diaria de movimientos


@router.get("/daily")
async def investment_evolution(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    type: str = "income",
):
    return await investment_evolution_v1(start_date, end_date, type)
