from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models import Category, Movement
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from io import StringIO, BytesIO
import csv
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


async def by_category_report_csv_v1(
    start_date: date,
    end_date: date,
    db: AsyncSession,
):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )

    category_by_date = await db.scalar(
        select(Category.name, func.sum(Movement.amount))
        .join(Category, Category.id == Movement.category_id)
        .filter(Movement.date >= start_date)
        .filter(Movement.date <= end_date)
        .group_by(Category.name)
    )

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


async def by_category_report_xslx_v1(
    start_date: date,
    end_date: date,
    db: AsyncSession,
):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )

    category_by_date = await db.scalar(
        select(Category.name, func.sum(Movement.amount))
        .join(Category, Category.id == Movement.category_id)
        .filter(Movement.date >= start_date)
        .filter(Movement.date <= end_date)
        .group_by(Category.name)
    )

    wb = Workbook()
    ws = wb.active

    headers = ["Category", "Total"]
    ws.append(headers)  # type: ignore

    for category, total in category_by_date:
        ws.append([category, total])  # type: ignore

    file_stream = BytesIO()
    wb.save(file_stream)

    file_stream.seek(0)

    filename = f"report_by_category_{start_date}_to_{end_date}.xslx"

    return StreamingResponse(
        content=file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attatchmen; filename={filename}"},
    )


async def by_category_report_pdf_v1(
    start_date: date,
    end_date: date,
    db: AsyncSession,
):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )

    category_by_date = await db.scalar(
        select(Category.name, func.sum(Movement.amount))
        .join(Category, Category.id == Movement.category_id)
        .filter(Movement.date >= start_date)
        .filter(Movement.date <= end_date)
        .group_by(Category.name)
    )

    buffer = BytesIO()

    # Crear documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Título con estilo
    title = Paragraph("OrderFlow Automatic Report by Category", styles["Title"])
    elements.append(title)  # type: ignore
    elements.append(Spacer(1, 12))  # type: ignore

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

    elements.append(table)  # type: ignore

    # Construir PDF
    doc.build(elements)  # type: ignore
    buffer.seek(0)

    return StreamingResponse(
        content=buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report_by_category.pdf"},
    )
