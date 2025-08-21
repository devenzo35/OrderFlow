from fastapi import APIRouter, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Category, Movement
from typing import Annotated
from ...dependencies import get_db
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from io import StringIO, BytesIO
import csv
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


router = APIRouter(
    prefix="/api/v1/export",
    tags=["Export V1"],
    responses={status.HTTP_400_BAD_REQUEST: {"message": "URL Not Found"}},
)


@router.get("/by-category/csv")
def export_category_report_csv(
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

    filename = f"report_by_category_{start_date}_to_{end_date}.csv"

    return StreamingResponse(
        content=output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attatchmen; filename={filename}"},
    )


@router.get("/by-category/xlsx")
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

    wb = Workbook()
    ws = wb.active

    headers = ["Category", "Total"]
    ws.append(headers)

    for category, total in category_by_date:
        ws.append([category, total])

    file_stream = BytesIO()
    wb.save(file_stream)

    file_stream.seek(0)

    filename = f"report_by_category_{start_date}_to_{end_date}.xslx"

    return StreamingResponse(
        content=file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attatchmen; filename={filename}"},
    )


@router.get("/by-category/pdf")
def export_pdf_category_report(
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

    buffer = BytesIO()

    # Crear documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Título con estilo
    title = Paragraph("OrderFlow Automatic Report by Category", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Encabezado de la tabla
    table_data = [["Category", "Total Amount"]] + [
        [cat, f"${amt:.2f}"] for cat, amt in category_by_date
    ]

    # Estilo de tabla
    table = Table(table_data, colWidths=[250, 150])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.gray),
            ]
        )
    )

    elements.append(table)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)

    return StreamingResponse(
        content=buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report_by_category.pdf"},
    )
