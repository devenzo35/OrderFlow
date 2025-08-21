from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.services.exports import (
    by_category_report_csv_v1,
    by_category_report_pdf_v1,
    by_category_report_xslx_v1,
)
from ...dependencies import get_db

from datetime import date


router = APIRouter(
    prefix="/api/v1/export",
    tags=["Export V1"],
    responses={status.HTTP_400_BAD_REQUEST: {"message": "URL Not Found"}},
)


@router.get("/by-category/csv")
async def export_category_report_csv(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    db: Session = Depends(get_db),
):
    return await by_category_report_csv_v1(start_date, end_date, db)


@router.get("/by-category/xlsx")
async def export_category_report_xlsx(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    db: Session = Depends(get_db),
):
    return await by_category_report_xslx_v1(start_date, end_date, db)


@router.get("/by-category/pdf")
async def export_pdf_category_report(
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    db: Session = Depends(get_db),
):
    return await by_category_report_pdf_v1(start_date, end_date, db)
