#!/usr/bin/env python3
"""Render the generated RTPC/DSP DOCX to a deterministic, reviewable PDF.

This is a local fallback for hosts where Word/Pages automation is unavailable.
It preserves document order, headings, paragraphs, and tables, and uses an
embedded Unicode font so Chinese engineering notation remains searchable.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentType
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph as PdfParagraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCX = ROOT / "VehicleSoundSynthV3_车机RTPC_DSP链路技术说明.docx"
DEFAULT_PDF = ROOT / "VehicleSoundSynthV3_车机RTPC_DSP链路技术说明.pdf"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
FONT_NAME = "VSSUnicode"
ACCENT = colors.HexColor("#C53D2F")
INK = colors.HexColor("#17202A")
MUTED = colors.HexColor("#58636F")
GRID = colors.HexColor("#BFC7CE")
PALE = colors.HexColor("#F3F5F7")


def iter_blocks(parent: DocumentType):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield DocxTable(child, parent)


def clean(text: str) -> str:
    return html.escape(text.strip()).replace("\n", "<br/>")


def has_page_break(paragraph: Paragraph) -> bool:
    return bool(paragraph._p.xpath('.//w:br[@w:type="page"]'))


def paragraph_flowable(paragraph: Paragraph, styles: dict[str, ParagraphStyle]):
    text = paragraph.text.strip()
    if not text:
        return Spacer(1, 5)
    style_name = paragraph.style.name
    if style_name.startswith("Heading 1"):
        style = styles["h1"]
    elif style_name.startswith("Heading 2"):
        style = styles["h2"]
    elif style_name.startswith("Heading 3"):
        style = styles["h3"]
    elif "+-----------" in text or ("drive_simulator" in text and "\n" in paragraph.text):
        style = styles["diagram"]
    elif any(token in text for token in (" = ", "clamp(", "pow(", "log10(", "y[n]", "Q")) and len(text) < 260:
        style = styles["formula"]
    else:
        style = styles["body"]
    return PdfParagraph(clean(text), style)


def table_flowable(table: DocxTable, styles: dict[str, ParagraphStyle], usable_width: float):
    rows: list[list[PdfParagraph]] = []
    max_cols = max((len(row.cells) for row in table.rows), default=1)
    for row_index, row in enumerate(table.rows):
        cell_style = styles["cell_header"] if row_index == 0 else styles["cell"]
        values = [PdfParagraph(clean(cell.text), cell_style) for cell in row.cells]
        values.extend(PdfParagraph("", styles["cell"]) for _ in range(max_cols - len(values)))
        rows.append(values)
    if not rows:
        return Spacer(1, 1)

    widths = []
    first = table.rows[0].cells
    raw = [max(int(cell._tc.tcPr.tcW.w or 1), 1) for cell in first]
    if len(raw) == max_cols and sum(raw) > 0:
        widths = [usable_width * value / sum(raw) for value in raw]
    else:
        widths = [usable_width / max_cols] * max_cols

    pdf_table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#253746")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for idx in range(1, len(rows)):
        if idx % 2 == 0:
            commands.append(("BACKGROUND", (0, idx), (-1, idx), PALE))
    pdf_table.setStyle(TableStyle(commands))
    return pdf_table


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "VSSBody", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=8.4, leading=12.2, textColor=INK, spaceAfter=5,
        ),
        "h1": ParagraphStyle(
            "VSSH1", parent=base["Heading1"], fontName=FONT_NAME,
            fontSize=17, leading=21, textColor=ACCENT, spaceBefore=12,
            spaceAfter=7, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "VSSH2", parent=base["Heading2"], fontName=FONT_NAME,
            fontSize=12.5, leading=16, textColor=INK, spaceBefore=9,
            spaceAfter=5, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "VSSH3", parent=base["Heading3"], fontName=FONT_NAME,
            fontSize=10.2, leading=13, textColor=MUTED, spaceBefore=7,
            spaceAfter=4, keepWithNext=True,
        ),
        "formula": ParagraphStyle(
            "VSSFormula", parent=base["Code"], fontName=FONT_NAME,
            fontSize=7.7, leading=10.6, textColor=colors.HexColor("#26384A"),
            backColor=colors.HexColor("#EEF2F5"), borderPadding=5,
            borderColor=colors.HexColor("#D1D8DE"), borderWidth=0.4,
            spaceBefore=3, spaceAfter=5,
        ),
        "diagram": ParagraphStyle(
            "VSSDiagram", parent=base["Code"], fontName="Courier",
            fontSize=6.9, leading=9.0, textColor=INK, leftIndent=3,
            spaceBefore=3, spaceAfter=5,
        ),
        "cell": ParagraphStyle(
            "VSSCell", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=6.7, leading=8.5, textColor=INK, alignment=TA_LEFT,
        ),
        "cell_header": ParagraphStyle(
            "VSSCellHeader", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=6.7, leading=8.5, textColor=colors.white, alignment=TA_LEFT,
        ),
        "footer": ParagraphStyle(
            "VSSFooter", parent=base["Normal"], fontName=FONT_NAME,
            fontSize=6.5, leading=8, textColor=MUTED, alignment=TA_CENTER,
        ),
    }


def render(docx_path: Path, pdf_path: Path) -> None:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Unicode font not found: {FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    styles = make_styles()
    page_width, page_height = letter
    left = right = 0.72 * inch
    top, bottom = 0.72 * inch, 0.62 * inch
    usable_width = page_width - left - right

    document = BaseDocTemplate(
        str(pdf_path), pagesize=letter, leftMargin=left, rightMargin=right,
        topMargin=top, bottomMargin=bottom,
        title="VehicleSoundSynth V3 车机 RTPC / DSP 链路技术说明",
        author="VehicleSoundSynth V3 Engineering",
    )
    frame = Frame(left, bottom, usable_width, page_height - top - bottom, id="body")

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(1.2)
        canvas.line(left, page_height - 0.46 * inch, page_width - right, page_height - 0.46 * inch)
        canvas.setFont(FONT_NAME, 6.4)
        canvas.setFillColor(MUTED)
        canvas.drawString(left, 0.33 * inch, "VehicleSoundSynth V3 · RTPC / DSP Technical Specification")
        canvas.drawRightString(page_width - right, 0.33 * inch, f"{doc.page}")
        canvas.restoreState()

    document.addPageTemplates(PageTemplate(id="all", frames=[frame], onPage=decorate))
    source = Document(str(docx_path))
    story = []
    for block in iter_blocks(source):
        if isinstance(block, Paragraph):
            if has_page_break(block):
                story.append(PageBreak())
            flowable = paragraph_flowable(block, styles)
            story.append(flowable)
        else:
            story.append(table_flowable(block, styles, usable_width))
            story.append(Spacer(1, 7))
    document.build(story)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docx", type=Path, default=DEFAULT_DOCX)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()
    render(args.docx.resolve(), args.pdf.resolve())
    print(args.pdf.resolve())


if __name__ == "__main__":
    main()
