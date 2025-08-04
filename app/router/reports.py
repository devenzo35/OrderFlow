from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Annotated
from datetime import datetime, timezone, date

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


# Resumen mensual agrupado por tipo
@router.get("/month-summary")
def get_monthly_report(
    year: Annotated[int, Query(ge=2000, le=2100)] = datetime.now(timezone.utc).year,
):

    # [
    #   {
    #     "month": "2025-01",
    #     "income": 1250.0,
    #     "expense": 700.0,
    #     "investment": 300.0
    #   },
    #   ...
    # ]
    return None


@router.get("/by-category")
def report_by_category(
    start_date: Annotated[date, Query()], end_date: Annotated[date, Query()]
):

    # [
    #   { "category_id": 1, "category_name": "Alquiler", "total": 3200.0 },
    #   { "category_id": 2, "category_name": "Comida", "total": 1550.0 }
    # ]
    return None


# Tendencia diaria de movimientos


@router.get("daily")
def report_daily_and_type(
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
