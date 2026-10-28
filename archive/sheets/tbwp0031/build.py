#!/usr/bin/env python3
"""Typeset what-is-open.md. Do not hand-edit the PDF."""

from pathlib import Path

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).resolve().parent
SRC = HERE / "what-is-open.md"
OUT = HERE / "what-is-open.pdf"

pdfmetrics.registerFont(TTFont("LibSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Italic", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibMono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"))

PAGE_W, PAGE_H = letter
LEFT = 0.7 * inch
RIGHT = 0.7 * inch
TOP = 0.72 * inch
BOTTOM = 0.62 * inch


def esc(text):
    return (
        text.replace("&", "&")
        .replace("<", "<")
        .replace(">", ">")
    )


def mono_bits(text):
    out = []
    parts = text.split("`")
    for i, part in enumerate(parts):
        bit = esc(part)
        if i % 2:
            out.append(f'<font face="LibMono" size="9">{bit}</font>')
        else:
            out.append(bit)
    return "".join(out)


BODY = ParagraphStyle(
    "body",
    fontName="LibSerif",
    fontSize=10.5,
    leading=14,
    alignment=TA_LEFT,
    spaceAfter=8,
)
H1 = ParagraphStyle(
    "h1",
    fontName="LibSerif-Bold",
    fontSize=16,
    leading=20,
    spaceAfter=8,
)
H2 = ParagraphStyle(
    "h2",
    fontName="LibSerif-Bold",
    fontSize=12,
    leading=16,
    spaceBefore=10,
    spaceAfter=6,
)
CELL = ParagraphStyle(
    "cell",
    fontName="LibSerif",
    fontSize=9,
    leading=12,
)
HEAD = ParagraphStyle(
    "head",
    fontName="LibSerif-Bold",
    fontSize=9,
    leading=12,
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("LibSerif", 8)
    canvas.drawString(LEFT, 0.38 * inch, "tbwp0031")
    canvas.drawRightString(PAGE_W - RIGHT, 0.38 * inch, str(doc.page))
    canvas.restoreState()


def parse(text):
    story = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(mono_bits(line[2:].strip()), H1))
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(mono_bits(line[3:].strip()), H2))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            data_rows = [r for r in rows if not all(set(c) <= set("-:") for c in r)]
            if not data_rows:
                continue
            header, body = data_rows[0], data_rows[1:]
            table_data = [[Paragraph(mono_bits(c), HEAD) for c in header]]
            for row in body:
                table_data.append([Paragraph(mono_bits(c), CELL) for c in row])
            widths = [7.1 * inch * 0.62, 7.1 * inch * 0.38]
            if len(header) == 1:
                widths = [7.1 * inch]
            table = Table(table_data, colWidths=widths, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("FONTNAME", (0, 0), (-1, 0), "LibSerif-Bold"),
                        ("BACKGROUND", (0, 0), (-1, 0), "#f0f0f0"),
                        ("GRID", (0, 0), (-1, -1), 0.25, "#666666"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 8))
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|")):
            para.append(lines[i].strip())
            i += 1
        story.append(Paragraph(mono_bits(" ".join(para)), BODY))
    return story


def main():
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=letter,
        title="What Instructor115 has open",
        author="tbwp0031",
    )
    frame = Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT, PAGE_H - TOP - BOTTOM, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])
    doc.build(parse(SRC.read_text()))
    print(OUT)


if __name__ == "__main__":
    main()
