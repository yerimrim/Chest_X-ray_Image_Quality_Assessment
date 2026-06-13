import os
import re
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (getSampleStyleSheet, ParagraphStyle)
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle
)

PRIMARY_COLOR = colors.HexColor("#2C3E50")
BG_LIGHT = colors.HexColor("#F8FAFC")
BORDER_COLOR = colors.HexColor("#E2E8F0")

COLOR_ACCEPT = "#2563EB" 
COLOR_REJECT = "#DC2626"  


def natural_sort_key(text):
    return [
        int(c) if c.isdigit()
        else c.lower()
        for c in re.split(r'(\d+)', text)
    ]


def add_image_if_exists(elements, image_path, title, styles):
    if os.path.exists(image_path):
        elements.append(Paragraph(title, styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(Image(image_path, width=420, height=260))
        elements.append(Spacer(1, 25))

def create_table(data):
    table = Table(data, colWidths=[150, 60, 80, 200] ,repeatRows=1, splitByRow=True)
    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                PRIMARY_COLOR
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "WORDWRAP",
                (0, 0),
                (-1, -1),
                "CJK"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    BG_LIGHT
                ]
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER_COLOR
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                PRIMARY_COLOR
            )
        ])
    )

    return table


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PRIMARY_COLOR)
    canvas.rect(0, doc.pagesize[1] - 40, doc.pagesize[0], 40, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(doc.leftMargin, doc.pagesize[1] - 25, "Medical Image Quality Assessment")
    canvas.setFillColor(colors.grey)
    canvas.setFont("Helvetica",9)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 30, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf(df):
    os.makedirs("outputs", exist_ok=True)
    pdf_path = ("outputs/quality_report.pdf")
    doc = SimpleDocTemplate(pdf_path, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=50)
    styles = getSampleStyleSheet()
    body_style = styles["BodyText"]
    elements = []

    title_style = ParagraphStyle(name="Title", parent=styles["Title"], alignment=TA_CENTER, fontSize=24, textColor=PRIMARY_COLOR)
    section_style = ParagraphStyle(name="Section", parent=styles["Heading1"], textColor=PRIMARY_COLOR)

    elements.append(Paragraph("Medical Image Quality Report", title_style))
    elements.append(Spacer(1, 20))

    total = len(df)
    accept = (df["status"] == "Accept").sum()
    reject = (df["status"] == "Reject").sum()
    accept_rate = (accept / total * 100) if total > 0 else 0

    elements.append(Paragraph("Executive Summary", section_style))
    summary = [
        ["Total Images", total],
        ["Accepted", accept],
        ["Rejected", reject],
        ["Acceptance Rate", f"{accept_rate:.2f}%"],
        ["Average Brightness", f"{df['brightness'].mean():.2f}"],
        ["Average Contrast", f"{df['contrast'].mean():.2f}"],
        ["Average Sharpness", f"{df['sharpness'].mean():.2f}"]
    ]

    summary_table = Table(summary, colWidths=[200, 200])
    summary_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Visualizations", section_style))
    chart_paths = [
        ("static/charts/grade.png", "Quality Grade Distribution"),
        ("static/charts/status.png", "Accept vs Reject Distribution"),
        ("static/charts/brightness.png", "Brightness Distribution"),
        ("static/charts/sharpness.png", "Sharpness Distribution")
    ]
    
    for path, title in chart_paths:
        add_image_if_exists(elements, path, title, styles)

    elements.append(PageBreak())
    elements.append(Paragraph("Image Details", section_style))

    table_data = [["Image", "Grade", "Status", "Reason"]]
    sorted_df = (df.sort_values(by="image_name", key=lambda x: x.map(natural_sort_key)))
    status_style = ParagraphStyle(
        name="StatusStyle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        alignment=TA_CENTER
    )

    for _, row in sorted_df.iterrows():
        status_value = str(row["status"])
        
        if status_value.strip().lower() in ["accept", "accepted"]:
            status_text = f'<font color="{COLOR_ACCEPT}">{status_value}</font>'
        elif status_value.strip().lower() in ["reject", "rejected"]:
            status_text = f'<font color="{COLOR_REJECT}">{status_value}</font>'
        else:
            status_text = status_value

        table_data.append([
            Paragraph(str(row["image_name"]), body_style),
            Paragraph(str(row["grade"]), body_style),
            Paragraph(status_text, status_style),
            Paragraph(str(row["reason"]), body_style)
        ])

    elements.append(create_table(table_data))
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    return pdf_path