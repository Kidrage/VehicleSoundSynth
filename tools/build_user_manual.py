#!/usr/bin/env python3
"""Build the Chinese VehicleSoundSynth operator and tuning manual.

Run with a Python environment that provides python-docx:
    python tools/build_user_manual.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "VehicleSoundSynthV5_完整使用手册.docx"

# compact_reference_guide preset; CJK font is a named glyph-support override.
BASE_FONT = "Calibri"
CJK_FONT = "PingFang SC"
MONO_FONT = "Menlo"
BLUE = "2E74B5"
DARK_BLUE = "1F4D78"
INK_BLUE = "0B2545"
MUTED = "5B6573"
HEADER_FILL = "E8EEF5"
LIGHT_FILL = "F2F4F7"
CALLOUT_FILL = "F4F6F9"
CAUTION_FILL = "FFF4CE"
CAUTION_TEXT = "7A5A00"
RISK_FILL = "FDECEC"
RISK_TEXT = "9B1C1C"
WHITE = "FFFFFF"
CONTENT_DXA = 9360
TABLE_INDENT_DXA = 120
CELL_MARGIN_DXA = {"top": 80, "bottom": 80, "start": 120, "end": 120}


def set_run_font(
    run,
    *,
    size: float | None = None,
    bold: bool | None = None,
    italic: bool | None = None,
    color: str | None = None,
    ascii_font: str = BASE_FONT,
    cjk_font: str = CJK_FONT,
) -> None:
    run.font.name = ascii_font
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.get_or_add_rFonts()
    fonts.set(qn("w:ascii"), ascii_font)
    fonts.set(qn("w:hAnsi"), ascii_font)
    fonts.set(qn("w:eastAsia"), cjk_font)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for side, value in CELL_MARGIN_DXA.items():
        tag = "start" if side == "start" else "end" if side == "end" else side
        node = tc_mar.find(qn(f"w:{tag}"))
        if node is None:
            node = OxmlElement(f"w:{tag}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color: str = "C8D1DC", size: int = 6) -> None:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), str(size))
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), color)


def set_fixed_table_geometry(table, widths_dxa: list[int]) -> None:
    if sum(widths_dxa) != CONTENT_DXA:
        raise ValueError(f"table widths must total {CONTENT_DXA}: {widths_dxa}")
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl = table._tbl
    tbl_pr = tbl.tblPr

    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(CONTENT_DXA))
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(TABLE_INDENT_DXA))
    tbl_ind.set(qn("w:type"), "dxa")

    layout = tbl_pr.first_child_found_in("w:tblLayout")
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    grid = tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for index, cell in enumerate(row.cells):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.first_child_found_in("w:tcW")
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(widths_dxa[index]))
            tc_w.set(qn("w:type"), "dxa")
            cell.width = Inches(widths_dxa[index] / 1440)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)
    set_table_borders(table)


def set_paragraph_background(paragraph, fill: str) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    shd = p_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        p_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_paragraph_border_bottom(paragraph, color: str = BLUE, size: int = 12) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = p_bdr.find(qn("w:bottom"))
    if bottom is None:
        bottom = OxmlElement("w:bottom")
        p_bdr.append(bottom)
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "8")
    bottom.set(qn("w:color"), color)


def add_page_field(paragraph) -> None:
    paragraph.add_run("第 ")
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run = paragraph.add_run()
    run._r.extend([begin, instr, separate, text, end])
    paragraph.add_run(" 页")


def add_numbering_definition(doc: Document, *, kind: str) -> int:
    numbering = doc.part.numbering_part.element
    abstract_ids = [
        int(node.get(qn("w:abstractNumId")))
        for node in numbering.findall(qn("w:abstractNum"))
        if node.get(qn("w:abstractNumId"))
    ]
    abstract_id = max(abstract_ids, default=-1) + 1
    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    lvl.append(start)
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "bullet" if kind == "bullet" else "decimal")
    lvl.append(num_fmt)
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "•" if kind == "bullet" else "%1.")
    lvl.append(lvl_text)
    lvl_jc = OxmlElement("w:lvlJc")
    lvl_jc.set(qn("w:val"), "left")
    lvl.append(lvl_jc)
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "540")
    tabs.append(tab)
    p_pr.append(tabs)
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "540")
    ind.set(qn("w:hanging"), "270")
    p_pr.append(ind)
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:after"), "80")
    spacing.set(qn("w:line"), "300")
    spacing.set(qn("w:lineRule"), "auto")
    p_pr.append(spacing)
    lvl.append(p_pr)
    r_pr = OxmlElement("w:rPr")
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), BASE_FONT)
    r_fonts.set(qn("w:hAnsi"), BASE_FONT)
    r_fonts.set(qn("w:eastAsia"), CJK_FONT)
    r_pr.append(r_fonts)
    lvl.append(r_pr)
    abstract.append(lvl)
    numbering.append(abstract)

    num_ids = [
        int(node.get(qn("w:numId")))
        for node in numbering.findall(qn("w:num"))
        if node.get(qn("w:numId"))
    ]
    num_id = max(num_ids, default=0) + 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), str(abstract_id))
    num.append(abstract_ref)
    numbering.append(num)
    return num_id


def apply_numbering(paragraph, num_id: int) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num = OxmlElement("w:numId")
    num.set(qn("w:val"), str(num_id))
    num_pr.extend([ilvl, num])
    p_pr.insert(0, num_pr)


def configure_styles(doc: Document) -> None:
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = BASE_FONT
    normal._element.rPr.rFonts.set(qn("w:ascii"), BASE_FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), BASE_FONT)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), CJK_FONT)
    normal.font.size = Pt(11)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25

    for style_name, size, color, before, after in (
        ("Heading 1", 16, BLUE, 18, 10),
        ("Heading 2", 13, BLUE, 14, 7),
        ("Heading 3", 12, DARK_BLUE, 10, 5),
    ):
        style = styles[style_name]
        style.font.name = BASE_FONT
        style._element.rPr.rFonts.set(qn("w:ascii"), BASE_FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), BASE_FONT)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), CJK_FONT)
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def configure_section(section) -> None:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.right_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)


def add_running_furniture(section, *, first_page: bool = False) -> None:
    section.different_first_page_header_footer = first_page
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("VehicleSoundSynth V6  |  使用与调音手册")
    set_run_font(run, size=8.5, color=MUTED)
    set_paragraph_border_bottom(p, color="D7DBE2", size=6)
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    add_page_field(fp)
    for run in fp.runs:
        set_run_font(run, size=8.5, color=MUTED)


def add_text(doc, text: str, *, bold_prefix: str | None = None):
    p = doc.add_paragraph()
    if bold_prefix and text.startswith(bold_prefix):
        lead = p.add_run(bold_prefix)
        set_run_font(lead, bold=True)
        rest = p.add_run(text[len(bold_prefix) :])
        set_run_font(rest)
    else:
        run = p.add_run(text)
        set_run_font(run)
    return p


def add_bullets(doc, items: list[str]) -> None:
    num_id = add_numbering_definition(doc, kind="bullet")
    for item in items:
        p = doc.add_paragraph()
        apply_numbering(p, num_id)
        run = p.add_run(item)
        set_run_font(run)


def add_steps(doc, items: list[str]) -> None:
    num_id = add_numbering_definition(doc, kind="decimal")
    for item in items:
        p = doc.add_paragraph()
        apply_numbering(p, num_id)
        run = p.add_run(item)
        set_run_font(run)


def add_code(doc, text: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.right_indent = Inches(0.18)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.05
    set_paragraph_background(p, "F7F8FA")
    run = p.add_run(text)
    set_run_font(run, size=9, color=INK_BLUE, ascii_font=MONO_FONT, cjk_font=CJK_FONT)


def add_callout(doc, title: str, body: str, *, kind: str = "info") -> None:
    fill, color = {
        "info": (CALLOUT_FILL, DARK_BLUE),
        "caution": (CAUTION_FILL, CAUTION_TEXT),
        "risk": (RISK_FILL, RISK_TEXT),
    }[kind]
    table = doc.add_table(rows=1, cols=1)
    set_fixed_table_geometry(table, [CONTENT_DXA])
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    lead = p.add_run(title + "  ")
    set_run_font(lead, bold=True, color=color)
    rest = p.add_run(body)
    set_run_font(rest, color=INK_BLUE)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_table(
    doc,
    headers: list[str],
    rows: list[list[str]],
    widths_dxa: list[int],
    *,
    font_size: float = 9.2,
) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    set_fixed_table_geometry(table, widths_dxa)
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for idx, header in enumerate(headers):
        cell = table.rows[0].cells[idx]
        set_cell_shading(cell, HEADER_FILL)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(header)
        set_run_font(r, size=font_size, bold=True, color=INK_BLUE)
    for row_index, values in enumerate(rows):
        cells = table.add_row().cells
        for idx, value in enumerate(values):
            cell = cells[idx]
            if row_index % 2:
                set_cell_shading(cell, "FAFBFC")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(str(value))
            set_run_font(r, size=font_size, color="1F2937")
    set_fixed_table_geometry(table, widths_dxa)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_heading(doc, text: str, level: int = 1) -> None:
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, bold=True)


def add_cover(doc: Document) -> None:
    doc.add_paragraph().paragraph_format.space_after = Pt(92)
    kicker = doc.add_paragraph()
    kicker.alignment = WD_ALIGN_PARAGRAPH.CENTER
    kicker.paragraph_format.space_after = Pt(18)
    run = kicker.add_run("MAX/MSP VEHICLE ACOUSTICS")
    set_run_font(run, size=10.5, bold=True, color=BLUE)
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(9)
    run = title.add_run("VehicleSoundSynth V6")
    set_run_font(run, size=30, bold=True, color=INK_BLUE)
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(12)
    run = subtitle.add_run("完整使用与拟真调音手册")
    set_run_font(run, size=18, bold=True, color=DARK_BLUE)
    desc = doc.add_paragraph()
    desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    desc.paragraph_format.space_after = Pt(74)
    run = desc.add_run("座舱低频轰鸣 · 燃油生命周期 · 七速 DCT · 四段总线 EQ")
    set_run_font(run, size=11.5, color=MUTED)
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_after = Pt(4)
    run = meta.add_run("手册版本 4.0  |  适用 Max 8.6.5  |  2026-08-12")
    set_run_font(run, size=10.5, bold=True, color=INK_BLUE)
    meta2 = doc.add_paragraph()
    meta2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta2.paragraph_format.space_after = Pt(0)
    run = meta2.add_run("项目分支：codex/vehicle-sound-v4  |  V1/V2/V3 保持独立不变")
    set_run_font(run, size=9, italic=True, color=MUTED)
    doc.add_page_break()


def build_v1_document(output: Path) -> None:
    doc = Document()
    configure_styles(doc)
    for section in doc.sections:
        configure_section(section)
    add_running_furniture(doc.sections[0], first_page=True)
    add_cover(doc)

    add_heading(doc, "内容导航", 1)
    add_text(doc, "本手册同时面向直接试听的使用者、接入车辆状态的 Max 开发者，以及希望继续提高拟真度的声音设计人员。建议首次使用按第 1-4 章操作，调音时再查阅第 5-9 章。")
    add_steps(
        doc,
        [
            "系统定位与声音链路",
            "安装、打开与 3 分钟快速启动",
            "主界面与三种 Drive Source",
            "外部状态接入",
            "全部实时可调参数",
            "三套预设与混音规则",
            "拟真调音方法",
            "高级内部参数与二次开发",
            "故障排查、测试与验收",
        ],
    )
    add_callout(
        doc,
        "范围说明",
        "“Future EV / High-Rev V12 / Aggressive V10”是三种声学方向，不是对 Porsche、Ferrari 或 Lamborghini 某一车型的认证复刻。当前系统是可运行的最小程序化原型，重点是驾驶反馈和可调性。",
        kind="info",
    )

    add_heading(doc, "1. 系统定位与声音链路", 1)
    add_text(doc, "VehicleSoundSynth 用车辆状态消息实时驱动三个程序化动力声源，并叠加换挡/爆鸣/机械点击瞬态、速度相关路噪以及座舱总线处理，最终输出受保护的立体声。它不依赖长循环发动机采样，因此适合快速塑造新声学 DNA，也便于后续迁移到 C++、Wwise 或车载 DSP。")
    add_table(
        doc,
        ["阶段", "模块", "主要输入", "职责"],
        [
            ["状态", "drive_simulator / vss.input", "油门、制动、速度、RPM、挡位与事件", "产生或接收统一车辆状态消息"],
            ["动力", "powertrain~ + 3 × gen~", "RPM、油门、负载、5 个音色宏", "EV、V12、V10 三种连续声源与实时混合"],
            ["细节", "transient~ / road_air~", "shift、pop、click、速度、亮度", "短促事件、路面/气流连续噪声"],
            ["座舱", "cabin_master~", "亮度、厚度、侵略性、声场宽度", "M/S 宽度、低通、增益、峰值保护"],
            ["输出", "main.maxpat", "Audio 开关", "60 ms 淡入淡出、电平表/频谱监看、立体声 DAC"],
        ],
        [1050, 1920, 2600, 3790],
    )
    add_callout(
        doc,
        "安全链路",
        "系统启动时 DSP 与最终音频门均为关闭状态；cabin_master~ 还含 omx.peaklim~ 与 ±0.891 硬限幅。它们是最后防线，不能代替低监听音量和循序加大电平。",
        kind="caution",
    )

    add_heading(doc, "2. 安装、打开与 3 分钟快速启动", 1)
    add_heading(doc, "2.1 运行条件", 2)
    add_bullets(
        doc,
        [
            "Cycling '74 Max 8.6.5；仅使用 Max/MSP/Gen 内置对象。",
            "双声道音频输出。首次使用耳机时先把系统音量和声卡旋钮调低。",
            "完整打开 VehicleSoundSynth.maxproj；不要只双击某个子 patch，否则搜索路径与媒体文件可能无法解析。",
        ],
    )
    add_heading(doc, "2.2 快速启动", 2)
    add_steps(
        doc,
        [
            "在 Finder 或 Max 中打开 VehicleSoundSynth.maxproj。",
            "在 Project 窗口打开 main.maxpat。若控件拖动而不是响应，按 Cmd+E 将 patcher 锁定。",
            "确认 Drive Source 为 Internal Manual，Preset 为 Future EV；把监听音量降到安全位置。",
            "点击 main.maxpat 左上方 Audio 开关。该开关同时启用全局 DSP，并用 60 ms 斜坡打开输出。",
            "在 Manual Throttle 输入 0.15，听到轻微动力声后逐渐增加到 0.5；Manual Brake 可用于降低内部目标车速。",
            "切换到 Internal Auto 可听约 10 秒周期的自动加减速；再依次试听 High-Rev V12 与 Aggressive V10。",
            "观察左右 meter~ 与 spectroscope~。确认没有持续顶格后再提高监听电平。",
        ],
    )
    add_callout(
        doc,
        "不要只点击底部 ezdac~",
        "主界面顶部 Audio 开关还控制最终 60 ms 音频门。即使底部 ezdac~ 已亮，顶部开关为 0 时仍会静音；日常操作以顶部开关为准。",
        kind="caution",
    )
    doc.add_page_break()
    add_heading(doc, "2.3 项目目录", 2)
    add_table(
        doc,
        ["路径", "用途"],
        [
            ["VehicleSoundSynth.maxproj", "Max 工程入口与 patchers/gen/media/presets 搜索路径"],
            ["main.maxpat", "可直接试听的操作界面"],
            ["patchers/vehicle_engine~.maxpat", "可复用的公共引擎：1 个消息入口、2 个音频出口"],
            ["patchers/*.maxpat", "动力、瞬态、路噪/气流、座舱母线、内部驾驶模拟器"],
            ["gen/*.gendsp", "EV、V12、V10 三个程序化动力声源"],
            ["media/*.wav", "48 kHz 单声道 shift/pop/click 瞬态样本"],
            ["presets/sound_dna.json", "三套预设的可读 JSON 数据"],
            ["tools/build_project.py", "确定性再生成 Max patch、Gen、媒体和预设"],
        ],
        [2700, 6660],
    )

    add_heading(doc, "3. 主界面与 Drive Source", 1)
    add_heading(doc, "3.1 三种状态源", 2)
    add_table(
        doc,
        ["模式", "适用场景", "行为与注意事项"],
        [
            ["Internal Manual", "快速试听、手动调音", "Throttle 与 Brake 驱动内置简化车辆模型；默认启动模式。"],
            ["Internal Auto", "循环试听、比较预设", "50 ms 更新一次；有效油门约 0.15-0.95，约 10 秒完成一个正弦变化周期，并自动产生挡位与 shift 脉冲。"],
            ["External vss.input", "遥测、游戏、传感器、其他 Max patch", "只接收命名消息；内部驾驶模拟器仍运行但被 selector 隔离，不进入声音引擎。"],
        ],
        [1800, 2500, 5060],
    )
    add_heading(doc, "3.2 内部驾驶模型（当前实现）", 2)
    add_text(doc, "该模型不是车辆动力学仿真，而是用于稳定试听的状态发生器。关键关系如下：")
    add_code(
        doc,
        "target_speed = clip(throttle × 260 - brake × 180, 0, 300) kph\n"
        "rpm = clip(650 + speed_kph × 31 + throttle × 1400, 0, 10000)\n"
        "load = clip(throttle × 1.6, -1, 1)\n"
        "accel = clip(throttle × 2 - brake × 2, -1, 1)\n"
        "gear = 0 (<1 kph)，否则 clip(int(speed_kph / 45) + 1, 1, 6)"
    )
    add_bullets(
        doc,
        [
            "速度上升与下降使用不同平滑量；制动后不会瞬间跳到新速度。",
            "挡位变化时自动发送 shift 1，80 ms 后发送 shift 0，从而触发换挡冲击样本。",
            "内部模型不会自动触发 pop 与 click；可在外部模式或直接使用 vehicle_engine~ 时发送。",
        ],
    )
    add_heading(doc, "3.3 预设、DNA 权重与宏参数", 2)
    add_text(doc, "Preset 菜单会立即把一组权重与宏参数发送到 engine。下方 EV/V12/V10 Weight 和 5 个宏参数是手动覆盖入口，任何模式下都直接作用于引擎。")
    add_callout(
        doc,
        "界面读数说明",
        "当前预设消息不会回写下方 flonum。因此下方数字表示“最近一次手动输入”，不一定等于当前引擎中的预设值。判断当前基线请看 Preset 菜单与第 6 章预设表。",
        kind="info",
    )

    add_heading(doc, "4. 外部状态接入", 1)
    add_heading(doc, "4.1 最小 Max 接法", 2)
    add_steps(
        doc,
        [
            "把 Drive Source 切换为 External vss.input。",
            "在任意 Max patch 中建立 [s vss.input]。",
            "把命名消息送入该对象，例如 speed_kph 80.、rpm 4200.、throttle 0.55。",
            "连续参数持续更新；事件参数只在事件发生时发送值 1，并可随后发送 0。",
        ],
    )
    add_code(
        doc,
        "[message: speed_kph 80.]  ->  [s vss.input]\n"
        "[message: rpm 4200.]       ->  [s vss.input]\n"
        "[message: throttle 0.55]   ->  [s vss.input]\n"
        "[message: load 0.40]       ->  [s vss.input]\n"
        "[message: shift 1]         ->  [s vss.input]"
    )
    add_heading(doc, "4.2 推荐更新策略", 2)
    add_table(
        doc,
        ["信号", "推荐更新/平滑起点", "原因"],
        [
            ["RPM / motor speed", "50-100 Hz；20-50 ms 平滑", "音高最敏感，低速率会产生阶梯感，过重平滑会削弱跟脚性。"],
            ["Throttle / load / torque", "50-100 Hz；10-30 ms 平滑", "需要保留脚感，又要抑制遥测抖动。"],
            ["Vehicle speed", "20-50 Hz；100-300 ms 平滑", "主要驱动路噪/风噪，可比动力声慢。"],
            ["Brake / accel / gear", "状态变化时立即发送", "供当前契约与后续模块扩展；当前声音映射有限。"],
            ["shift / pop / click", "单帧或 20-100 ms 脉冲", "sel 1 触发一次样本；不要每一帧重复发送 1。"],
        ],
        [1900, 2900, 4560],
    )
    add_callout(
        doc,
        "遥测归一化",
        "先在接入层统一单位和范围，再发送到合成器。不要把车轮 RPM 当发动机 RPM，也不要直接把未经限幅的扭矩百分比送入 load。若数据丢失，保持最后有效值并在 200-500 ms 内安全回落。",
        kind="caution",
    )
    doc.add_page_break()
    add_heading(doc, "4.3 直接复用引擎抽象", 2)
    add_text(doc, "若不使用 main.maxpat，可在自己的 patch 中放置 [vehicle_engine~]：左侧 inlet 接收本手册中的 18 种命名消息，两个 outlet 为左右声道。外部工程仍应通过 VehicleSoundSynth.maxproj 或把 patchers、gen、media 加入 Max Search Path。")

    add_heading(doc, "5. 全部实时可调参数", 1)
    add_heading(doc, "5.1 车辆状态参数", 2)
    add_table(
        doc,
        ["消息", "范围/单位", "当前实际作用", "使用建议"],
        [
            ["speed_kph", "0-300 km/h", "road_air~ 的幅度；内部模型还用它计算 RPM 与挡位。", "真实车辆接入时用滤波后的车速；声音上不应随单帧抖动。"],
            ["rpm", "0-10000 rpm", "三种 Gen 动力声的基频/点火阶次。", "燃油车用发动机转速；EV 可映射为电机/虚拟转速。"],
            ["throttle", "0-1", "动力声幅度；内部模型同时决定速度、RPM、load、accel。", "踏板与扭矩并不等价；拟真时应与 load 分开。"],
            ["brake", "0-1", "当前引擎接受但无独立声层；内部模型降低目标速度并影响 accel。", "后续用于制动啸叫、再生制动与轮胎负载。"],
            ["load", "-1-1", "动力声幅度；EV 使用绝对值，V12/V10 只使用正负载。", "正值驱动、负值滑行/再生；这是拟真的核心状态之一。"],
            ["accel", "-1-1", "当前公共契约接受，但尚未直接连接声源。", "建议后续驱动轮胎滑移、车身冲击和情绪瞬态。"],
            ["gear", "0-6", "当前公共契约接受；直接发送 gear 不会自动触发 shift。", "挡位变化时同时发送 shift 1；0 表示驻车/无挡。"],
            ["shift", "0 或 1", "值 1 播放 shift_thump.wav；基础增益 0.50。", "事件触发，不要持续保持或高频重复 1。"],
            ["pop", "0 或 1", "值 1 播放 exhaust_pop.wav；基础增益 0.38。", "适用于燃油风格收油/换挡；EV 预设通常关闭。"],
            ["click", "0 或 1", "值 1 播放 mechanical_click.wav；基础增益 0.24。", "少量用于继电器、齿轮或座舱机械感。"],
        ],
        [1500, 1500, 3400, 2960],
        font_size=8.7,
    )
    add_callout(
        doc,
        "契约与映射不是同一件事",
        "brake、accel、gear 已被公共接口接受，便于保持统一车辆状态，但当前 MVP 还没有为它们建立独立声学映射；这不是接入错误。",
        kind="info",
    )
    add_heading(doc, "5.2 DNA 权重与音色宏", 2)
    add_table(
        doc,
        ["消息", "范围", "作用位置", "听感与风险"],
        [
            ["ev_weight", "0-1", "EV Gen 输出，40 ms 平滑", "提高未来感电机/逆变器声；与其他权重相加会提高总电平。"],
            ["v12_weight", "0-1", "V12 Gen 输出，40 ms 平滑", "提高平顺、高转、谐波密集的燃油声。"],
            ["v10_weight", "0-1", "V10 Gen 输出，40 ms 平滑", "提高半阶低频、点火主阶和 2.5 倍粗粝层。"],
            ["aggression", "0-1", "Gen、瞬态总增益、座舱总增益", "更直接、更响、更冲；也是最容易造成响度偏差的宏。"],
            ["brightness", "0-1", "Gen 谐波、路噪低通、座舱低通", "提高空气感与穿透力；过高易在 2-6 kHz 刺耳。"],
            ["body", "0-1", "Gen 基础/低阶成分、座舱增益", "增加厚度和质量感；当前也会整体增益变大。"],
            ["texture", "0-1", "三个 Gen 的逆变器/高阶/rasp", "增加电气、粗粝和金属细节；当前在 transient/cabin/road 中虽被路由但未参与 DSP。"],
            ["cabin_width", "0-1", "座舱 M/S 的 Side 增益", "映射为约 0.25-1.30 倍 Side；过宽可能导致单声道抵消。"],
        ],
        [1700, 1150, 2900, 3610],
        font_size=8.8,
    )
    add_heading(doc, "5.3 权重混合规则", 2)
    add_bullets(
        doc,
        [
            "三个权重分别在 0-1 内限幅并用 40 ms 线性斜坡平滑。",
            "权重是线性相加，不会自动归一化。1/0/0 是单一 EV；0.5/0.5/0 是 EV 与 V12 的各半叠加。",
            "权重和超过 1 时通常更响，可能更早触发 limiter；做公平 A/B 时建议让权重和约等于 1。",
            "三个权重都为 0 时，动力声消失，但路噪和事件层仍可发声。",
        ],
    )

    doc.add_page_break()
    add_heading(doc, "6. 三套预设", 1)
    add_table(
        doc,
        ["预设", "EV/V12/V10", "Agg./Bright.", "Body/Texture/Width", "设计意图"],
        [
            ["Future EV", "1.00 / 0 / 0", "0.25 / 0.72", "0.34 / 0.20 / 0.82", "平滑升频、较宽声场、较轻质感；接近高性能 EV 的未来主义提示音方向。"],
            ["High-Rev V12", "0 / 1.00 / 0", "0.62 / 0.78", "0.72 / 0.52 / 0.64", "高转、明亮、较平顺；强调主阶与 2/3 倍谐波。"],
            ["Aggressive V10", "0 / 0 / 1.00", "0.90 / 0.66", "0.84 / 0.86 / 0.56", "更厚、更粗粝、更靠前；突出半阶低频与 2.5 倍 rasp。"],
        ],
        [1700, 1600, 1450, 2150, 2460],
        font_size=8.7,
    )
    add_heading(doc, "6.1 从预设开始做自己的 DNA", 2)
    add_steps(
        doc,
        [
            "先选最接近的预设，把三个权重保持为单一声源；先不要混。",
            "用同一段 Internal Auto 循环，先调 Brightness 和 Body，找到频谱轮廓。",
            "再调 Aggression 对齐响度与响应；Texture 最后加入，避免用粗糙度掩盖音高/负载关系问题。",
            "调整 Cabin Width，并切到单声道检查是否变薄或丢失关键成分。",
            "如需混合第二声源，先从 0.05-0.20 开始，并降低主声源使总权重约为 1。",
            "记录数值到 presets/sound_dna.json；若要让主界面菜单使用新值，同时更新 tools/build_project.py 中 PRESETS 后再生成工程。",
        ],
    )

    doc.add_page_break()
    add_heading(doc, "7. 往拟真方向调：推荐顺序", 1)
    add_callout(
        doc,
        "先修“因果”，再修“音色”",
        "车辆声是否可信，首先取决于 RPM、负载、速度、换挡与收油的时间关系。只增加谐波或饱和度，往往只会得到更夸张的合成器。",
        kind="info",
    )
    add_steps(
        doc,
        [
            "状态标定：核对单位、范围、空转值、红线、挡位和负载正负方向。",
            "阶次标定：让音高与转速/电机极对/齿轮啮合存在稳定比例，而不是凭耳朵随意升频。",
            "负载动态：同一 RPM 下比较驱动、匀速、收油和再生；先把响度与频谱差异做对。",
            "事件动态：加入换挡扭矩切断、冲击、爆鸣、机械点击，并保证事件有原因且稀疏。",
            "道路与气流：让速度而非 RPM 驱动连续噪声；按轮胎、路面、风噪拆层。",
            "座舱与空间：最后做共振、吸声、宽度和扬声器/座舱响应，并重新做响度匹配。",
        ],
    )
    add_heading(doc, "7.1 Taycan 类高性能 EV 方向", 2)
    add_table(
        doc,
        ["目标", "当前可调起点", "建议新增/改造", "避免"],
        [
            ["电机主音随速度连续上升", "Future EV；brightness 0.60-0.78，texture 0.12-0.30", "把 EV 的 f=55+0.052×rpm 改成真实 motor_rpm × pole_pairs / 60 的电气阶次。", "低速就出现过大固定音量；主音与车速/RPM 不一致。"],
            ["逆变器与齿轮啮合细节", "texture 逐步增加，aggression 保持 0.15-0.35", "分开 inverter_order、gear_mesh_ratio、PWM carrier；各自有负载包络。", "用单一高频正弦代表所有电气噪声。"],
            ["收油/再生反馈", "外部发送负 load；当前 EV 使用 abs(load)", "拆分 drive_load 与 regen_load，让再生层音色和方向独立。", "把收油做成排气爆鸣；这会破坏 EV 身份。"],
            ["座舱未来感", "cabin_width 0.70-0.90，body 0.25-0.45", "加入少量不对称延迟、窄带模态与车型座舱 EQ/IR。", "过宽导致中心空洞，或 2-5 kHz 长时间刺耳。"],
        ],
        [1500, 2300, 3560, 2000],
        font_size=8.5,
    )
    add_heading(doc, "7.2 Ferrari 类高转 V12 方向", 2)
    add_bullets(
        doc,
        [
            "以 High-Rev V12 为起点：brightness 约 0.72-0.86，body 0.58-0.76，texture 0.40-0.62，aggression 0.50-0.70。",
            "当前主点火阶次 f=rpm/60×6，符合四冲程 V12 每转 6 次点火的简化关系；拟真重点是各阶次幅度随负载和 RPM 改变，而不是增加无限谐波。",
            "高转时让高阶逐步抬升、低阶稍收；收油时保留机械阶次但减少燃烧幅度。",
            "换挡应包含 60-120 ms 扭矩/幅度切断与恢复，再叠加 shift thump；爆鸣只在高负载收油等条件下概率触发。",
            "保持较窄但稳定的中心像，cabin_width 可从 0.52-0.70 起步；用座舱 EQ 增加空间，而非只拉宽 Side。",
        ],
    )
    add_heading(doc, "7.3 Lamborghini 类激进 V10 方向", 2)
    add_bullets(
        doc,
        [
            "以 Aggressive V10 为起点：aggression 0.72-0.92，body 0.72-0.90，texture 0.68-0.90，brightness 0.58-0.74。",
            "当前主阶次 f=rpm/60×5，并加入 0.5×f 低频和 2.5×f rasp；可把 rasp 做成带宽有限、随负载变化的噪声/谐波簇，而不是永远稳定的正弦。",
            "V10 的“凶”应来自点火不均匀感、进排气模态、机械噪声与瞬态，而不仅是总增益。先做调制，再加 aggression。",
            "shift/pop 比 V12 更可见，但仍要满足转速、负载和收油条件；建议为重复样本加入 2-4 个变体或轻微随机音高/电平。",
        ],
    )
    doc.add_page_break()
    add_heading(doc, "7.4 常见听感问题与调参方向", 2)
    add_table(
        doc,
        ["症状", "先检查", "建议调整", "风险"],
        [
            ["像静态合成器，不像车", "RPM/负载是否真实", "增强 load 对幅度与频谱的影响；加入收油、换挡扭矩切断。", "只加 texture 会更假。"],
            ["声音跟脚太慢", "上游与 Gen 平滑", "缩短 RPM/Throttle 平滑；事件保持即时。", "太短会暴露遥测阶梯和噪声。"],
            ["高频刺耳", "brightness、texture、2-6 kHz", "先降 brightness 0.05-0.15，再降 texture；降低座舱低通上限。", "别用 limiter 当 EQ。"],
            ["低频轰、没有转速感", "body 与 0.5×阶次", "降低 body/V10 low；高通路噪，避免多个低阶同相堆叠。", "过度削低频会失去质量感。"],
            ["混合预设突然变响", "三个权重之和", "让权重和约为 1，并做等响度校准。", "limiter 会掩盖响度错误并改变音色。"],
            ["声场很宽但中心空", "cabin_width 与单声道", "把宽度降到 0.5-0.8；减少左右固定失谐。", "宽度 >1 的 Side 放大可能单声道抵消。"],
            ["路噪盖住动力声", "speed_kph 与 brightness", "降低 speed_curve 的 0.32 系数；分拆轮胎与风噪。", "单纯降总高频会让动力也变闷。"],
        ],
        [1700, 1950, 3830, 1880],
        font_size=8.4,
    )

    doc.add_page_break()
    add_heading(doc, "8. 高级内部参数与二次开发", 1)
    add_callout(
        doc,
        "生成文件规则",
        "main.maxpat、patchers/*.maxpat、gen/*.gendsp、media/*.wav 与 presets/sound_dna.json 由 tools/build_project.py 生成。需要改结构或 DSP 常数时编辑生成器，再运行生成命令；不要直接改生成文件，否则下次会被覆盖。",
        kind="risk",
    )
    add_heading(doc, "8.1 当前动力声公式", 2)
    add_table(
        doc,
        ["声源", "频率关系", "幅度/构成", "当前平滑与限幅"],
        [
            ["EV", "f=clip(55+0.052×rpm,55,760 Hz)；逆变器≈f×(2.8+brightness)", "core + inverter + 1.013×f air；幅度=0.03+0.25×throttle+0.08×|load|", "RPM slide 1200/1800 samples；Throttle 700/1400；±0.78"],
            ["V12", "f=clip(rpm/60×6,35,1000 Hz)", "f、2f、3f；幅度=0.025+0.30×throttle+0.10×positive_load", "RPM 1000/1600；Throttle 650/1200；±0.80"],
            ["V10", "f=clip(rpm/60×5,32,850 Hz)", "0.5f low + f fire + 2.5f rasp；幅度=0.03+0.33×throttle+0.12×positive_load", "RPM 850/1300；Throttle 500/900；±0.82"],
        ],
        [1050, 2450, 3650, 2210],
        font_size=8.3,
    )
    add_text(doc, "在 48 kHz 下，1200 samples 约为 25 ms，1800 samples 约为 37.5 ms。Gen 的 slide 参数是样本计数，不要误当毫秒。")
    add_heading(doc, "8.2 连续噪声、瞬态与座舱", 2)
    add_table(
        doc,
        ["模块", "当前关键常数", "拟真升级建议"],
        [
            ["road_air~", "speed_gain=(speed/300)^0.7×0.32；高通 65 Hz；低通截止=700+6500×brightness；120 ms 幅度平滑", "拆为 tire/road/wind 三层；加入 surface、slip、wetness、crosswind；风噪高通可从 1.5-2 kHz 试起。"],
            ["transient~", "shift/pop/click 基础增益 0.50/0.38/0.24；aggression 映射 0.7-1.3；左右 0.96/0.88", "事件条件化、样本变体、音高/电平随机、换挡扭矩切断；EV 与燃油车使用不同事件集。"],
            ["cabin_master~", "brightness→4.5-19 kHz 低通；body→0.78-1.03 增益；aggression→0.48-0.68 增益；width→0.25-1.30 Side", "加入座舱模态、扬声器/座椅传递函数或短 IR；把 body/aggression 的音色与总响度解耦。"],
            ["master", "omx.peaklim~ 后接 clip~ ±0.891", "以 -18/-12 dBFS 校准层级，保留 6 dB 以上瞬态余量；limiter 只处理偶发峰值。"],
        ],
        [1650, 3710, 4000],
        font_size=8.5,
    )
    add_heading(doc, "8.3 最值得新增的可调参数", 2)
    add_table(
        doc,
        ["建议参数", "建议范围/类型", "控制对象", "优先级"],
        [
            ["motor_pole_pairs", "1-12 整数", "EV 电气主阶次", "高"],
            ["inverter_order / pwm_carrier", "1-12 / 2-16 kHz", "逆变器阶次与载波", "高"],
            ["gear_mesh_ratio", "5-40 × motor order", "减速器/齿轮啮合音", "高"],
            ["torque / regen_load", "-1-1 分拆", "驱动与再生的不同包络", "高"],
            ["harmonic_tilt / roughness", "-12-+6 dB/oct / 0-1", "谐波衰减与不规则度", "高"],
            ["shift_cut_ms / recovery_ms", "30-150 / 50-300 ms", "换挡前后的动力幅度", "中"],
            ["tire_mix / wind_mix / surface", "0-1 / 0-1 / 枚举", "连续车辆噪声", "高"],
            ["cabin_mode / cabin_ir_mix", "预设 / 0-1", "座舱共振或卷积", "中"],
            ["saturation / exhaust_resonance", "0-1 / 50-800 Hz", "燃油排气非线性与管路模态", "中"],
            ["master_trim_db", "-24-0 dB", "预设等响度与安全余量", "高"],
        ],
        [2350, 2150, 3460, 1400],
        font_size=8.6,
    )
    add_heading(doc, "8.4 再生成与验证", 2)
    add_code(
        doc,
        "cd /Users/saintpeter/Downloads/VehicleSoundSynth\n"
        "python3 tools/build_project.py\n"
        "python3 -m unittest discover -s tests -v"
    )
    add_text(doc, "生成器是确定性的：同一源码应产生相同输出。当前测试覆盖公共接口、Gen 参数、媒体格式、搜索路径、输出保护、UI 元素、patch cord 端口有效性与重复生成一致性。")

    doc.add_page_break()
    add_heading(doc, "9. 故障排查、测试与验收", 1)
    add_heading(doc, "9.1 常见问题", 2)
    add_table(
        doc,
        ["现象", "检查顺序", "处理"],
        [
            ["完全无声", "顶部 Audio→Max Audio Status→输出设备→Throttle/RPM→权重", "先选 Future EV 和 Internal Auto；确保顶部 Audio 为 1，并把 EV Weight 设为 1。"],
            ["底部扬声器亮但无声", "顶部 Audio 是否为 0", "用顶部 Audio 开关；它还控制最终 line~ 音频门。"],
            ["找不到 gen~ 或子 patch", "是否打开 maxproj、Search Path", "从 VehicleSoundSynth.maxproj 进入；确认 patchers/gen/media/presets 已在项目搜索路径。"],
            ["shift/pop/click 没声音", "事件是否发送精确值 1、媒体是否加载", "发送 shift 1 而不是只改 gear；检查 media/*.wav 和 Max Console。"],
            ["持续爆点/重复样本", "事件源是否每帧发送 1", "改为边沿触发；事件后发送 0，或在上游用 change/sel。"],
            ["声音刺耳或频繁压限", "权重和、aggression、body、brightness", "先把权重和降到 1，再降 aggression/body；最后才调 limiter。"],
            ["外部模式没有响应", "Drive Source 与 send 名称", "选择 External vss.input；对象必须是 [s vss.input]，消息名与大小写完全一致。"],
            ["修改 .maxpat 后又消失", "是否运行过生成器", "修改 tools/build_project.py，而不是生成文件。"],
        ],
        [1900, 3150, 4310],
        font_size=8.6,
    )
    add_heading(doc, "9.2 听音验收清单", 2)
    add_bullets(
        doc,
        [
            "冷启动安全：工程打开后无声；开启 Audio 时无明显爆音，关闭时平滑淡出。",
            "因果关系：RPM 决定主音高，throttle/load 决定能量，speed_kph 决定路噪；三者不会互相混淆。",
            "预设差异：EV、V12、V10 在相同状态下能被盲听区分，且不是单纯响度差。",
            "瞬态合理：shift/pop/click 只在事件发生时出现，不连发、不抢占连续声源。",
            "混音安全：任一单预设与常用混合都不持续顶格；limiter 不应长时间明显抽吸。",
            "单声道兼容：将左右声道相加后，核心动力声不应大幅消失。",
            "动态连续：慢扫 RPM 与油门时无阶梯、断裂、异常跳音；快速动作又不过分迟钝。",
            "A/B 一致：比较预设或版本时匹配主观响度，否则“更响”会被误判为“更好”。",
        ],
    )
    add_heading(doc, "9.3 推荐测试场景", 2)
    add_table(
        doc,
        ["场景", "输入", "要听什么"],
        [
            ["静止怠速/待机", "0 kph，650 rpm，throttle 0", "底噪、固定啸叫是否过大；EV 是否能合理安静。"],
            ["定转负载扫描", "固定 3000 rpm，load -1→1", "负载变化是否有明确但连续的音色/能量反馈。"],
            ["全转速慢扫", "650→红线，throttle 0.5", "阶次连续、无混叠感、无突然增益跳变。"],
            ["快速点踩", "throttle 0→1→0", "攻击与回落是否跟脚，是否有 click/pop 误触发。"],
            ["换挡", "gear n→n+1 + shift pulse", "动力切断、冲击与恢复是否形成一个事件。"],
            ["高速滑行", "120-250 kph，throttle 0", "路噪/风噪是否随速度存在，动力声是否合理回落。"],
            ["立体声/单声道", "width 0→1 并折叠 mono", "宽度改变但核心不消失，左右能量不过度失衡。"],
        ],
        [1800, 2850, 4710],
        font_size=8.7,
    )

    doc.add_page_break()
    add_heading(doc, "附录 A：消息速查", 1)
    add_code(
        doc,
        "speed_kph 0..300    rpm 0..10000       throttle 0..1\n"
        "brake 0..1          load -1..1         accel -1..1\n"
        "gear 0..6           shift 0|1          pop 0|1          click 0|1\n"
        "ev_weight 0..1      v12_weight 0..1    v10_weight 0..1\n"
        "aggression 0..1     brightness 0..1    body 0..1\n"
        "texture 0..1        cabin_width 0..1"
    )
    add_heading(doc, "附录 B：最小外部测试序列", 1)
    add_code(
        doc,
        "ev_weight 1.\n"
        "v12_weight 0.\n"
        "v10_weight 0.\n"
        "aggression 0.25\n"
        "brightness 0.72\n"
        "body 0.34\n"
        "texture 0.20\n"
        "cabin_width 0.82\n"
        "speed_kph 60.\n"
        "rpm 3000.\n"
        "throttle 0.45\n"
        "load 0.35"
    )
    add_callout(
        doc,
        "结束操作",
        "试听结束先关闭 main.maxpat 顶部 Audio，再关闭 Max DSP 或音频接口。保存自定义数值时记录全部 3 个权重与 5 个宏，避免只记录局部状态。",
        kind="caution",
    )

    # Apply explicit font settings to all runs, including text created by python-docx.
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.font.name is None:
                set_run_font(run)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name is None:
                            set_run_font(run)

    core = doc.core_properties
    core.title = "VehicleSoundSynth 完整使用与拟真调音手册"
    core.subject = "Max/MSP 车辆声学合成器的操作、参数、接入、拟真调音与二次开发"
    core.author = "VehicleSoundSynth Project"
    core.keywords = "Max/MSP, Vehicle Sound, EV, V12, V10, 使用手册, 调音"
    core.comments = "Generated from the VehicleSoundSynth implementation baseline cfc59a0."

    settings = doc.settings.element
    update_fields = settings.find(qn("w:updateFields"))
    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)
    update_fields.set(qn("w:val"), "true")

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    audit_document(output)


def build_document(output: Path) -> None:
    """Build the V6 compact operator reference without overwriting prior manuals."""
    doc = Document()
    configure_styles(doc)
    configure_section(doc.sections[0])
    add_running_furniture(doc.sections[0], first_page=True)
    add_cover(doc)

    add_heading(doc, "1. V6 是什么", 1)
    add_text(
        doc,
        "VehicleSoundSynth V6 从冻结的 V4 稳定版分支而来，保留三个独立 runtime、连续油门/RPM 与七速 DCT，并增加无采样的 BEAP 回火、V10/V12 电影 Pad、共享可保存 EQ 和更有辨识度的怠速机体声。",
    )
    add_callout(
        doc,
        "版本边界",
        "V6 位于 VehicleSoundSynth-V6 文件夹，入口是 VehicleSoundSynth-V6.maxproj。V1、V2、V3 与冻结的 V4 文件夹和旧版手册均保持原样。",
        kind="caution",
    )
    add_callout(
        doc,
        "拟真边界",
        "V12/V10 根据四冲程点火阶次、负载包络和共振谐波构建，是可调的程序化声学 archetype，并非对某一量产车型录音的测量匹配复刻。用于正式车型前仍应与参考录音做盲听和频谱校准。",
        kind="info",
    )
    add_table(
        doc,
        ["层级", "模块", "职责"],
        [
            ["状态与生命周期", "drive_simulator / engine_controller", "速度、RPM、七速挡位、点火启动、换挡削扭与事件时序"],
            ["连续声源", "powertrain~ / Gen", "EV、四冲程 V12、四冲程 V10；燃油声受 engine_running 门控"],
            ["座舱低频", "cabin_rumble~ / MSP", "真实 powertrain 信号激励 48/68/92/118 Hz 阻尼模态、结构振动与排气轰鸣"],
            ["瞬态与环境", "transient~ / road_air~", "CC0 启动机、升降挡、回火、爆音/crackle；粉红轮胎与受控白噪风声"],
            ["座舱与播出", "cabin_master~ / mix_master~", "120 Hz 以下收中、上频段相位/早反射扩宽、可视化四节点 EQ 与唯一 limiter/clip"],
        ],
        [1800, 2700, 4860],
    )

    add_heading(doc, "2. 第一次打开：按这个顺序", 1)
    add_steps(
        doc,
        [
            "先把监听音量调低。在 Finder 或 Max 中打开 VehicleSoundSynth-V6.maxproj，并等待 Project 窗口完成加载。",
            "从同一个 Max 实例的 Project 窗口打开 main.maxpat。不要同时双击工程与 main，否则搜索路径可能尚未注册。",
            "在 Preset 选择 High-Rev V12 或 Aggressive V10。",
            "把 Ignition 打开，再单击 Engine Start。先确认启动机和怠速已经进入电平表。",
            "最后打开顶部 Audio。它同时打开 60 ms 输出淡入和 ezdac~；关闭时会平滑淡出。",
            "把 Drive Source 切到 Internal Auto，听完整的升挡、降挡、收油与回火过程。",
        ],
    )
    add_callout(
        doc,
        "为什么燃油预设不会一选就响",
        "V12/V10 默认 engine_running=0，这是有意设计。必须 Ignition=1 后触发 Start，约 500 ms 启动机阶段结束，连续燃烧声才淡入。Future EV 不受燃油生命周期门控。",
        kind="info",
    )

    add_heading(doc, "3. 主界面控制", 1)
    add_table(
        doc,
        ["控制", "范围/动作", "实际作用"],
        [
            ["Drive Source", "Manual / Auto / External", "选择内置手动、20 秒自动驾驶循环或 r vss.input 外部状态"],
            ["Throttle / Brake", "0-1", "内置模型的加速与制动；Auto 模式会自动驱动"],
            ["Preset", "EV / V12 / V10", "同时设置 engine_type、声源权重、宏参数与安全总线 trim"],
            ["Ignition / Engine Start", "开关 / 按钮", "只启动燃油 profile；点火关闭会停止启动机与燃烧声"],
            ["EV/V12/V10 Weight", "0-1", "连续混合三个声源；手动混合不自动归一化"],
            ["五个宏", "0-1", "Aggression、Brightness、Body、Texture、Cabin Width"],
            ["三个低频宏", "0-1", "Cabin Rumble、Exhaust Boom、Structure Vibration；Future EV 默认全部为 0"],
            ["四个 Stem Level", "-60..+6 dB", "Powertrain、Transient、Road、Rumble 独立 50 ms 平滑增益"],
            ["Pad / Ferrari Texture", "dB、Mute、Solo", "Pad 与 EV 电机并列；Solo 只静音 EV 电机。Ferrari 纹理只用于 V10/V12"],
            ["Cabin IR Mix", "0-1", "原声与 4096 tap 车舱 IR 的等功率湿/干混合"],
            ["Global EQ", "可视化四节点", "拖动曲线节点，或选 0-3 后输入 Frequency/Gain/Q；与 eq_* 消息同步"],
            ["EQ Bypass / Master Trim", "0/1；-24..0 dB", "30 ms 平滑干湿旁路；50 ms 输出增益平滑"],
        ],
        [2100, 1900, 5360],
    )

    add_heading(doc, "4. V12/V10 声学、怠速与座舱轰鸣", 1)
    add_text(doc, "EV Pad 的 120 Hz 以下会先合成为严格居中的 Mid；只有 120 Hz 以上使用 82/18 左右互混，因此保留左右音色差异的同时，不会在 mono 折叠时丢失底部能量。")
    add_text(doc, "燃油 Gen 使用四冲程点火阶次：V12 主阶为 rpm/60×6，V10 主阶为 rpm/60×5。左右声道现在分别模拟两个真实缸列：每个缸列以总点火率的一半工作，右缸列固定错开半个缸列周期，并以少量交叉馈送保持相位稳定，不再使用微失谐制造拍频。主声由点火脉冲、二至八阶加法谐波、±3% 以内的循环差异与脉冲门控窄带燃烧残差共同构成；燃油 Gen 不再注入白噪声。")
    add_table(
        doc,
        ["Profile", "默认怠速方向", "主要特征", "安全建议"],
        [
            ["High-Rev V12", "约 780 rpm", "39/78 Hz 阶次、较平顺车身模态、随转速抬升的 2/3/5/8 次谐波", "默认低频 0.90/0.62/0.58；Master Trim -8 dB"],
            ["Aggressive V10", "约 850 rpm", "35.4/70.8 Hz 阶次、更强结构振动、1.5/2.5 倍粗粝侧带", "默认低频 0.92/0.74/0.72；Master Trim -8 dB"],
        ],
        [1900, 1500, 3860, 2100],
    )
    add_bullets(
        doc,
        [
            "待机必须能听到连续中低频，但不能依赖 limiter 把过响信号压平。",
            "换挡时 shift_cut 会在约 90 ms 内把燃烧增益压到 0.22 后恢复。",
            "Brightness 主要影响上部谐波；觉得像电车啸叫时，先减 0.05-0.15，而不是增加 Body。",
        ],
    )

    add_heading(doc, "5. 三个低频控制怎样配合", 1)
    add_table(
        doc,
        ["控制", "主要频段/来源", "听感与使用方式"],
        [
            ["Structure Vibration", "约 28-70 Hz；发动机半阶与机脚/车身传递", "决定座椅和车体的慢速震动感；过大会发软或触发 limiter"],
            ["Cabin Rumble", "约 44-126 Hz；48/68/92/118 Hz 模态", "决定车内持续压力和怠速包围感，是最直接的座舱轰鸣旋钮"],
            ["Exhaust Boom", "约 35-110 Hz；半阶、点火主阶与二阶", "随油门和负载增强；用于加速和高挡低转速的排气重量"],
        ],
        [2100, 2800, 4460],
    )
    add_callout(
        doc,
        "低频安全",
        "低频层在约 28 Hz 高通；IR 湿/干混合后用 cross~ 120 将 120 Hz 以下合成严格居中的 Mid，上频段才进入左右不同的短 allpass 和 0.65/1.35 ms 早反射。中频 Side 安全系数为 0.20，高频为 0.42，交叉反射为 0.04，所以低频兼容 mono、机械细节仍有宽度。最后仍经过全局 EQ、Master Trim 和唯一的 limiter/clip。",
        kind="caution",
    )

    add_heading(doc, "6. 七速 DCT 与因果瞬态", 1)
    add_table(
        doc,
        ["事件", "触发原因", "声音结果"],
        [
            ["升挡", "profile 对应 RPM 超过上限且挡位 < 7", "shift_dir 1、升挡冲击变体、90 ms 削扭恢复"],
            ["降挡", "RPM 低于下限且挡位 > 1", "shift_dir -1、降挡冲击、排气 pop 与后续 crackle"],
            ["进气回火", "燃油 profile 下负载跨过 0.72", "intake_backfire 变体，约 90 ms 后复位"],
            ["手动爆音", "exhaust_pop 1 或 pop 1", "排气 pop，随后稀疏 crackle；EV profile 会被 gate 阻止"],
        ],
        [1450, 3550, 4360],
    )
    add_text(doc, "V12 速比：3.10 / 2.13 / 1.62 / 1.29 / 1.03 / 0.84 / 0.70。V10 速比：3.13 / 2.10 / 1.52 / 1.20 / 0.94 / 0.76 / 0.62。启动、换挡、回火、爆音、crackle 与机械细节均来自已处理的 CC0 现场录音；事件采用 round-robin 变体，避免连续触发出现完全相同的“机关枪”重复。")

    add_heading(doc, "7. 四段总线 EQ 与高频控制", 1)
    add_table(
        doc,
        ["频段", "默认", "用途", "常见调整"],
        [
            ["Low Shelf", "90 Hz / 0 dB", "车体重量、怠速底座", "缺重量可 +1~+3 dB；浑浊则减"],
            ["Low-Mid", "250 Hz / 0 dB / Q 0.8", "座舱轰鸣与箱体感", "闷、堵时在 180~350 Hz 减 1~4 dB"],
            ["High-Mid", "3.8 kHz / 0 dB / Q 1.0", "机械咬合、刺耳感", "优先在 2.5~5 kHz 减 1~5 dB"],
            ["High Shelf", "9 kHz / 0 dB", "空气感与高频噪声", "高频偏多时从 -2~-6 dB 开始"],
        ],
        [1600, 2050, 2700, 3010],
    )
    add_callout(
        doc,
        "最终保护只有一处",
        "信号顺序是 powertrain/transient/road/cabin_rumble → cabin_master~ → mix_master~ 四段 EQ/trim → omx.peaklim~ → ±0.891 clip~。因此全局 EQ 会同时作用于发动机与新增低频层；cabin_master~ 不再二次限幅。",
        kind="info",
    )
    add_text(doc, "新的 EQ 只使用一张 nfilters=4 的 filtergraph~，系数列表同时送到左右 cascade~。曲线拖动、节点数值、eq_* 消息、Bypass 与 Reset 共用同一 DSP 路径，不再出现界面数值改变但音频仍绕过旧 biquad 的情况。")
    add_text(doc, "road_air~ 只有两类持续噪声：居中的 pink~ 轮胎床（约 70-900 Hz）和受控立体声 noise~ 风声（约 400-4000 Hz）。Road Level 默认 -16 dB；V10/V12 Gen 内已移除白噪声。")

    add_heading(doc, "8. 素材、归一化与拟真边界", 1)
    add_table(
        doc,
        ["来源", "运行用途", "处理/峰值"],
        [
            ["Grasopt — Car Starter", "V12/V10 启动机", "48 kHz PCM16、去 DC、淡入淡出、-3 dBFS"],
            ["TheLittleCrow — Engine contact", "三组升挡与三组降挡", "裁切、归一化至 -6 dBFS"],
            ["richwise — Sports/Supercar", "进气回火、排气 pop/crackle", "回火 -6、pop -5、crackle -8 dBFS"],
            ["microman502 — Gear shift", "机械 click 与 shift thump", "裁切、去 DC、-6 dBFS"],
            ["jamespeacock4616 — Mini car IR", "左右 4096 tap 车舱 IR", "每声道单独裁切、-3 dBFS"],
            ["用户 SF90 近场 Ferrari.wav", "本地双层去基频残差，仅 V10/V12", "1.0 s 起点/250 ms idle loop；22.75 s 起点/500 ms high-RPM loop；均为 -18 dBFS RMS，media/local 永不提交"],
        ],
        [2600, 3200, 3560],
        font_size=8.6,
    )
    add_callout(
        doc,
        "为什么仍不是录音级复刻",
        "短事件和 IR 已是真实录音，但连续 V12/V10 仍是程序化模型，没有同一辆车在多 RPM/多负载、进气/排气/机舱/座舱多麦克风条件下的同步测量，也没有卷积的机脚与车身传递函数。因此它比纯正弦原型更有机械结构，却仍属于可调 sound-design archetype。",
        kind="info",
    )
    add_text(doc, "全部来源、许可、原始/处理后 SHA-256、裁切点、帧数和归一化目标见 ASSET_LICENSES.md 与 assets/asset_manifest.json。build_project.py 不覆盖已经存在的 curated media。")

    add_heading(doc, "9. 外部状态接入", 1)
    add_text(doc, "把命名消息发送到 s vss.input，并把 Drive Source 设为 External。vehicle_engine~ 仍保持一个控制 inlet 与两个立体声 outlet。")
    add_code(
        doc,
        "engine_type v12     ignition 1          start 1\n"
        "speed_kph 80.       rpm 4200.           throttle 0.55\n"
        "brake 0.            load 0.62           accel 0.18\n"
        "gear 4              shift_dir 1         shift 1\n"
        "intake_backfire 1   exhaust_pop 1       click 1\n"
        "cabin_rumble 0.90   exhaust_boom 0.62   structure_vibration 0.58",
    )
    add_code(
        doc,
        "powertrain_level_db -3.   transient_level_db -7.\n"
        "road_level_db -16.        rumble_level_db -5.\n"
        "pad_level_db -3.          pad_mute 0            pad_solo 0\n"
        "reference_texture_level_db -24.   reference_texture_mute 0\n"
        "cabin_ir_mix 0.20",
    )
    add_text(doc, "EQ 消息格式：")
    add_code(
        doc,
        "eq_low 90. -2.\n"
        "eq_lowmid 250. -2.5 0.8\n"
        "eq_highmid 3800. -3. 1.0\n"
        "eq_high 9000. -4.\n"
        "eq_bypass 0\n"
        "master_trim_db -8.",
    )

    add_heading(doc, "10. 验证与故障排查", 1)
    add_table(
        doc,
        ["现象", "优先检查", "处理"],
        [
            ["燃油预设完全无声", "Ignition / Start / Audio", "先点火、启动，看到怠速电平后再开 Audio"],
            ["No such object / gen patcher not found", "工程是否先打开", "从 VehicleSoundSynth-V6.maxproj 进入，同一实例再开 main"],
            ["低频听不到", "监听设备与三个低频宏", "先确认设备能播放 35-120 Hz；提高 Cabin Rumble，再按需增加 Structure Vibration"],
            ["buffer~ can't open", "media 搜索路径", "确认 Project 的 media 搜索路径及所有生成 WAV 存在"],
            ["高频噪声过多", "road_air、Brightness、High-Mid/High Shelf", "先削 3.8 kHz 与 9 kHz，再判断是否需要减 Texture"],
            ["EQ 看似无效", "频段、Bypass、测量信号", "确认 EQ Bypass=0；峰值段在中心频率测；shelf 的标称频率是约 -6 dB 转折点"],
            ["某个 dB 不生效", "对应 stem 是否有信号", "EV 的 Rumble 默认 -60 dB；事件未触发时 Transient Level 不会改变持续电平"],
            ["换挡没有声音", "是否由 drive 产生 shift_dir", "Auto 模式试听；外部接入应在挡位变化时发送短脉冲"],
            ["声音很响或发硬", "Master Trim 与总线 EQ", "将 trim 退到 -9~-12 dB；不要把 limiter 当作响度控制"],
        ],
        [2200, 3000, 4160],
    )
    add_text(doc, "开发验证命令：")
    add_code(
        doc,
        "cd /Users/saintpeter/Downloads/VehicleSoundSynth-V6\n"
        "python3 tools/build_project.py --output-root .\n"
        "python3 -m unittest discover -s tests -v\n"
        "python3 tools/audio_metrics.py <render.wav> --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-low-side-ratio 0.05 --min-low-band-correlation 0.95 --max-mono-fold-rms-loss-db 1.5 --max-high-ratio 0.10 --min-spectral-peaks 6 --max-dominant-peak-ratio 0.50\n"
        "python3 tools/audio_metrics.py <high_rpm.wav> --compare-wav <ferrari_window.wav> --min-third-octave-similarity-left 0.85 --min-third-octave-similarity-right 0.85 --min-third-octave-similarity 0.87 --max-third-octave-similarity-lr-delta 0.05",
    )
    add_bullets(
        doc,
        [
            "Max Console 不应出现 invalid category、No such object、could not find gen patcher 或 patchcord outlet out of range。",
            "冷启动应无爆音；燃油 idle、加速、升挡、降挡、回火与滑行应分别试听。",
            "用 audio_metrics.py 检查 peak、RMS、30-140 Hz 轰鸣、20-30 Hz 次声、低频 Side/相关性、mono 折叠损失、1/3 倍频程相似度与 6-20 kHz 能量占比。",
        ],
    )

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.font.name is None:
                set_run_font(run)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name is None:
                            set_run_font(run)

    core = doc.core_properties
    core.title = "VehicleSoundSynth V6 完整使用与调音手册"
    core.subject = "Max/MSP 座舱低频轰鸣、多阶燃油车辆声学、CC0 瞬态、七速 DCT 与四段总线 EQ"
    core.author = "VehicleSoundSynth Project"
    core.keywords = "Max/MSP, Vehicle Sound, V12, V10, Cabin Rumble, DCT, EQ, 使用手册"
    core.comments = "Generated for VehicleSoundSynth V6; prior version manuals remain unchanged."
    settings = doc.settings.element
    update_fields = settings.find(qn("w:updateFields"))
    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)
    update_fields.set(qn("w:val"), "true")
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    audit_document(output)


def audit_document(path: Path) -> None:
    with ZipFile(path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        styles_xml = archive.read("word/styles.xml").decode("utf-8")
        numbering_xml = archive.read("word/numbering.xml").decode("utf-8")
        settings_xml = archive.read("word/settings.xml").decode("utf-8")

    checks = {
        "Letter page width": 'w:w="12240"' in document_xml,
        "Letter page height": 'w:h="15840"' in document_xml,
        "one-inch margins": all(token in document_xml for token in ('w:top="1440"', 'w:right="1440"', 'w:bottom="1440"', 'w:left="1440"')),
        "compact body line spacing": 'w:line="300"' in styles_xml,
        "heading color": BLUE in styles_xml,
        "real numbering definitions": "<w:abstractNum" in numbering_xml and "<w:numPr>" in document_xml,
        "fixed table width": f'w:w="{CONTENT_DXA}"' in document_xml,
        "table indent": f'w:w="{TABLE_INDENT_DXA}"' in document_xml,
        "update fields on open": "w:updateFields" in settings_xml,
        "no placeholders": not re.search(r"\b(TODO|TBD|PLACEHOLDER)\b", document_xml),
    }
    failures = [name for name, ok in checks.items() if not ok]
    if failures:
        raise RuntimeError("DOCX audit failed: " + ", ".join(failures))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_document(args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
