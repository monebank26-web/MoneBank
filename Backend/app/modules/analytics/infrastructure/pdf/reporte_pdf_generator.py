from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf_reporte(reporte: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("MoneBank — Reporte Financiero Mensual", styles["Title"]))
    elementos.append(Spacer(1, 12))

    periodo_texto = (
        f"Periodo: {reporte['periodo_inicio']} — {reporte['periodo_fin']}"
    )
    elementos.append(Paragraph(periodo_texto, styles["Normal"]))
    elementos.append(Spacer(1, 12))

    resumen_data = [
        ["Total Ingresos", f"${reporte['total_ingresos']:,.0f}"],
        ["Total Gastos", f"${reporte['total_gastos']:,.0f}"],
        ["Balance", f"${reporte['balance']:,.0f}"],
    ]
    tabla_resumen = Table(resumen_data, colWidths=[8 * cm, 6 * cm])
    tabla_resumen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("Detalle por categoría", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    detalle = reporte.get("detalle_por_categoria", [])
    if detalle:
        cabecera = ["Categoría", "Tipo", "Total"]
        filas = [cabecera] + [
            [d["nombre_categoria"], d["tipo_transaccion"], f"${d['total']:,.0f}"]
            for d in detalle
        ]
        tabla_detalle = Table(filas, colWidths=[6 * cm, 4 * cm, 4 * cm])
        tabla_detalle.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C9A24B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla_detalle)
    else:
        elementos.append(Paragraph("No hay movimientos registrados en este periodo.", styles["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer