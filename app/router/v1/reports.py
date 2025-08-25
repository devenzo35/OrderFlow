from fastapi import APIRouter, Depends, Request, status, Query
from typing import Annotated
from datetime import datetime, timezone, date
from app.schemas import MonthlyBalance, CategoryDistribution
from app.services.reports import (
    by_category_report_v1,
    investment_evolution_v1,
    monthly_report_v1,
)

from ...dependencies import get_db, default_limiter  # type: ignore
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports V1"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


# Resumen mensual agrupado por tipo
@router.get("/month-summary", response_model=MonthlyBalance)
@default_limiter  # type: ignore
async def get_monthly_report(
    request: Request,
    year: Annotated[int, Query()] = datetime.now(timezone.utc).year,
    month: Annotated[int, Query()] = datetime.now(timezone.utc).month,
    db: Session = Depends(get_db),
):
    return await monthly_report_v1(year, month, db)


@router.get("/by-category", response_model=list[CategoryDistribution])
@default_limiter  # type: ignore
async def by_category_report(
    request: Request,
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
@default_limiter  # type: ignore
async def investment_evolution(
    request: Request,
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    type: str = "income",
):
    return await investment_evolution_v1(start_date, end_date, type)
