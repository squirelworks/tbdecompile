#!/usr/bin/env python3
"""Typeset the TBdecompile reference manual.

One PDF is the whole book. The same book is also the separate sheets:
cover, table of contents, preface, foreword, the contents, and each
appendix. A sheet is split only when it would reach 100 pages, and only
between headings — never inside a paragraph, a table, a code block, or a
list item.

    python3 manual/build.py
    python3 manual/build.py front
"""

from __future__ import annotations

import html
import re
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "record"
MAPS = ROOT / "maps"
OLD_MAPS = ROOT / "trail" / "20261015" / "20261012"
OLD_PDF = ROOT / "editions" / "v0.0.1" / "TBdecompile_appendices.pdf"
SOURCES = Path(__file__).resolve().parent / "sources"
EDITION = ROOT / "manual" / "20261027"
BUNDLE = EDITION / "src"
OUT_DIRS = [EDITION]

PAGE_CAP = 100
# Leave headroom so a later small edit does not cross the cap on the same break.
PACK_LIMIT = 92
EDITION_DATE = "27 October 2026"
EDITION_LABEL = "v0.0.11"
SINGLE = f"TBdecompile-{EDITION_LABEL}.pdf"

pdfmetrics.registerFont(TTFont("LibSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Italic", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-BI", "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-Bold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibMono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"))

PAGE_W, PAGE_H = letter
LEFT = 0.7 * inch
RIGHT = 0.7 * inch
TOP = 0.72 * inch
BOTTOM = 0.62 * inch
FRAME_W = PAGE_W - LEFT - RIGHT


def S(name, **kw):
    base = dict(
        fontName="LibSerif",
        fontSize=10.5,
        leading=14,
        textColor="black",
        splitLongWords=0,
        encoding="utf-8",
    )
    base.update(kw)
    return ParagraphStyle(name, **base)


STYLES = {
    "h1": S("h1", fontName="LibSans-Bold", fontSize=16, leading=20, spaceBefore=14, spaceAfter=8),
    "h2": S("h2", fontName="LibSans-Bold", fontSize=13, leading=17, spaceBefore=12, spaceAfter=6),
    "h3": S("h3", fontName="LibSans-Bold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=4),
    "body": S("body", alignment=TA_JUSTIFY, spaceAfter=8),
    "li": S("li", alignment=TA_LEFT, spaceAfter=2, leading=13.5),
    "th": S("th", fontName="LibSans-Bold", fontSize=8, leading=10, alignment=TA_LEFT),
    "td": S("td", fontName="LibSerif", fontSize=8, leading=10, alignment=TA_LEFT),
    "title": S("title", fontName="LibSans-Bold", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=6),
    "subtitle": S("subtitle", fontName="LibSerif", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=4),
}


def inline(text: str, code_size: float = 9) -> str:
    """Markdown inline to reportlab XML. Code spans are taken out before emphasis, so a `*` inside code is not a tag."""
    pieces = []
    pos = 0
    for m in re.finditer(r"`([^`]+)`", text):
        pieces.append(("t", text[pos:m.start()]))
        pieces.append(("c", m.group(1)))
        pos = m.end()
    pieces.append(("t", text[pos:]))
    out = []
    for kind, chunk in pieces:
        if kind == "c":
            out.append(f'<font face="LibMono" size="{code_size}">{html.escape(chunk, quote=False)}</font>')
            continue
        t = html.escape(chunk, quote=False)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
        t = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", t)
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
        out.append(t)
    return "".join(out)


def parse_blocks(md: str):
    """Split markdown into blocks. A block is never a partial paragraph."""
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    blocks = []
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(("code", buf))
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*-+", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|?\s*-+", lines[i]):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            blocks.append((f"h{len(m.group(1))}", m.group(2).strip()))
            i += 1
            continue
        if re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", line):
            items = []
            ordered = bool(re.match(r"^\s*\d+\.", line))
            while i < len(lines) and re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^(\s*[-*+]|\s*\d+\.)\s+", "", lines[i]).strip())
                i += 1
                # continuation lines that are indented stay with the item
                while i < len(lines) and lines[i].startswith("  ") and not re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            blocks.append(("ol" if ordered else "ul", items))
            continue
        if line.strip() == "---":
            i += 1
            continue
        buf = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "```")) and not re.match(r"^(\s*[-*+]|\s*\d+\.)\s+", lines[i]) and lines[i].strip() != "---":
            buf.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(buf)))
    return blocks


def code_flowable(lines):
    # A short block is one paragraph per source line so a diagram is not reflowed.
    # A long block (a map, a listing) is one preformatted flowable. ReportLab splits
    # it between lines, not inside a line.
    if len(lines) > 40:
        text = "\n".join(line.replace("\t", "    ") for line in lines)
        style = S(
            "pre",
            fontName="LibMono",
            fontSize=8,
            leading=10,
            splitLongWords=0,
            spaceAfter=8,
        )
        return [Preformatted(text, style, maxLineLength=400, newLineChars="\n")]
    flows = []
    for raw in lines:
        text = raw.replace("\t", "    ")
        size = 8
        if text and pdfmetrics.stringWidth(text, "LibMono", 8) > FRAME_W - 4:
            size = 7
        escaped = html.escape(text).replace(" ", "&nbsp;")
        flows.append(
            Paragraph(
                f'<font face="LibMono" size="{size}">{escaped or "&nbsp;"}</font>',
                S(f"code{size}", fontName="LibMono", fontSize=size, leading=size + 2, spaceAfter=0, splitLongWords=0),
            )
        )
    if flows:
        flows[-1].spaceAfter = 8
    return flows


def table_flowable(rows):
    if not rows:
        return Spacer(1, 1)
    ncol = max(len(r) for r in rows)
    norm = [r + [""] * (ncol - len(r)) for r in rows]
    plain = [[re.sub(r"[`*]", "", c) for c in r] for r in norm]

    def mins_at(size):
        mins = []
        for j in range(ncol):
            longest = 8
            for r in norm:
                # Measure the tokens that will actually be drawn, including code spans at mono.
                raw = r[j]
                for tok in re.split(r"\s+", raw):
                    if not tok:
                        continue
                    bare = tok.replace("`", "").replace("*", "")
                    face = "LibMono" if "`" in raw else "LibSerif"
                    # A cell of mostly code is measured as mono so an address stays one line.
                    if "`" in tok or (tok.startswith("`") or tok.endswith("`")):
                        face = "LibMono"
                    longest = max(longest, pdfmetrics.stringWidth(bare, face, size))
            mins.append(longest + 8)
        return mins

    size = 8
    mins = mins_at(size)
    while sum(mins) > FRAME_W - 4 and size > 6:
        size -= 0.5
        mins = mins_at(size)
    if sum(mins) > FRAME_W - 4:
        # A single token is wider than the frame. Scale down together rather than cut the token.
        scale = (FRAME_W - 4) / sum(mins)
        widths = [m * scale for m in mins]
    else:
        leftover = FRAME_W - sum(mins)
        bulk = [1] * ncol
        for r in plain:
            for j, c in enumerate(r):
                bulk[j] += min(len(c), 40)
        bsum = sum(bulk)
        widths = [mins[j] + leftover * bulk[j] / bsum for j in range(ncol)]

    th = S(f"th{size}", fontName="LibSans-Bold", fontSize=size, leading=size + 2, alignment=TA_LEFT, splitLongWords=0)
    td = S(f"td{size}", fontName="LibSerif", fontSize=size, leading=size + 2, alignment=TA_LEFT, splitLongWords=0)
    data = []
    for ri, r in enumerate(norm):
        style = th if ri == 0 else td
        data.append([Paragraph(inline(c, code_size=size) if c else "&nbsp;", style) for c in r])
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), "#f0f0f0"),
                ("LINEBELOW", (0, 0), (-1, 0), 0.4, "#222222"),
                ("LINEBELOW", (0, 1), (-1, -2), 0.15, "#cccccc"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    tbl.splitByRow = 1
    tbl.spaceAfter = 8
    return tbl


def blocks_to_flowables(blocks, keep_headings=True):
    flows = []
    for kind, payload in blocks:
        if kind == "h1":
            flows.append(CondPageBreak(1.4 * inch))
            flows.append(Paragraph(inline(payload), STYLES["h1"]))
        elif kind == "h2":
            flows.append(CondPageBreak(1.1 * inch))
            flows.append(Paragraph(inline(payload), STYLES["h2"]))
        elif kind == "h3":
            flows.append(Paragraph(inline(payload), STYLES["h3"]))
        elif kind == "p":
            flows.append(Paragraph(inline(payload), STYLES["body"]))
        elif kind in ("ul", "ol"):
            items = []
            for it in payload:
                items.append(ListItem(Paragraph(inline(it), STYLES["li"]), leftIndent=12, bulletColor="black"))
            flows.append(
                ListFlowable(
                    items,
                    bulletType="1" if kind == "ol" else "bullet",
                    start="1" if kind == "ol" else "•",
                    leftIndent=16,
                    bulletFontName="LibSerif",
                    bulletFontSize=10,
                    spaceAfter=8,
                )
            )
        elif kind == "code":
            flows.extend(code_flowable(payload))
        elif kind == "table":
            flows.append(table_flowable(payload))
    return flows


class NumberedDoc(BaseDocTemplate):
    def __init__(self, path, header_left, header_right, bare=False):
        super().__init__(
            str(path),
            pagesize=letter,
            title=header_right or "TBdecompile",
            author="TBdecompile",
        )
        self.header_left = header_left
        self.header_right = header_right
        self.bare = bare
        frame = Frame(LEFT, BOTTOM, FRAME_W, PAGE_H - TOP - BOTTOM, id="normal", showBoundary=0)
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._decorate)])

    def _decorate(self, canvas, doc):
        if self.bare:
            return
        canvas.saveState()
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("LibSans", 8)
        canvas.drawString(LEFT, PAGE_H - 0.42 * inch, self.header_left)
        canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 0.42 * inch, f"Page {doc.page}")
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(0.4)
        canvas.line(LEFT, PAGE_H - 0.50 * inch, PAGE_W - RIGHT, PAGE_H - 0.50 * inch)
        canvas.setFont("LibSerif", 8)
        canvas.drawString(LEFT, 0.36 * inch, self.header_right)
        canvas.drawRightString(PAGE_W - RIGHT, 0.36 * inch, EDITION_DATE)
        canvas.restoreState()


def render(md: str, path: Path, header_left: str, header_right: str, bare=False) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = NumberedDoc(path, header_left, header_right, bare=bare)
    blocks = parse_blocks(md)
    if bare:
        story = []
        story.append(Spacer(1, 1.6 * inch))
        for kind, payload in blocks:
            if kind == "h1":
                story.append(Paragraph(inline(payload), STYLES["title"]))
            elif kind == "p":
                story.append(Paragraph(inline(payload), STYLES["subtitle"]))
            else:
                story.extend(blocks_to_flowables([(kind, payload)]))
    else:
        story = blocks_to_flowables(blocks)
    if not story:
        story = [Paragraph(" ", STYLES["body"])]
    doc.build(story)
    return len(PdfReader(str(path)).pages)


def section_splits(md: str, level: int):
    """Yield (heading, body) at a heading level. The heading line stays with its body."""
    pattern = re.compile(rf"(?m)^#{{{level}}} .*$")
    matches = list(pattern.finditer(md))
    if not matches:
        return [("document", md)]
    parts = []
    if matches[0].start() > 0:
        lead = md[: matches[0].start()].strip()
        if lead:
            parts.append(("front", lead + "\n"))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        heading = m.group(0).lstrip("#").strip()
        parts.append((heading, md[m.start() : end].rstrip() + "\n"))
    return parts


def pack(md: str, stem: str, header_left: str, header_right: str) -> list[tuple[str, int]]:
    """Render md. If it would be >= 100 pages, split between sections and pack."""
    primary = OUT_DIRS[0] / f"{stem}.pdf"
    pages = render(md, primary, header_left, header_right)
    if pages < PAGE_CAP:
        return [(stem, pages)]

    # Prefer chapter breaks, then section breaks. Never a paragraph.
    pieces = section_splits(md, 1)
    if len(pieces) < 2:
        pieces = section_splits(md, 2)
    if len(pieces) < 2:
        raise SystemExit(f"{stem} is {pages} pages and has no heading to split on")

    # Measure each piece on its own so packing is based on real pages.
    measured = []
    for i, (title, body) in enumerate(pieces):
        tmp = Path("/tmp") / f"tbmeasure-{stem}-{i}.pdf"
        n = render(body, tmp, header_left, header_right)
        if n >= PAGE_CAP:
            finer = section_splits(body, 2)
            if len(finer) < 2:
                finer = section_splits(body, 3)
            if len(finer) < 2:
                raise SystemExit(f"section {title!r} is {n} pages and cannot be split without cutting a paragraph")
            for j, (t2, b2) in enumerate(finer):
                tmp2 = Path("/tmp") / f"tbmeasure-{stem}-{i}-{j}.pdf"
                n2 = render(b2, tmp2, header_left, header_right)
                if n2 >= PAGE_CAP:
                    raise SystemExit(f"subsection {t2!r} is {n2} pages with no further heading")
                measured.append((t2, b2, n2))
        else:
            measured.append((title, body, n))

    groups = []
    cur_title = []
    cur_body = []
    cur_n = 0
    for title, body, n in measured:
        if cur_body and cur_n + n > PACK_LIMIT:
            groups.append((cur_title, cur_body, cur_n))
            cur_title, cur_body, cur_n = [], [], 0
        cur_title.append(title)
        cur_body.append(body)
        cur_n += n
    if cur_body:
        groups.append((cur_title, cur_body, cur_n))

    # Remove the oversize single render; write the parts.
    primary.unlink(missing_ok=True)
    written = []
    width = 2 if len(groups) < 100 else 3
    for i, (titles, bodies, _) in enumerate(groups, 1):
        part_stem = f"{stem}-{i:0{width}d}"
        text = "\n".join(bodies)
        # A one-line range note so a part is identifiable without cutting the source text.
        note = (
            f"This is part {i} of {len(groups)} of {header_right}. "
            f"It begins at “{titles[0]}” and ends at “{titles[-1]}”. "
            f"The previous part ended at a heading. No paragraph was divided.\n\n"
        )
        n = render(note + text, OUT_DIRS[0] / f"{part_stem}.pdf", header_left, header_right)
        if n >= PAGE_CAP:
            raise SystemExit(f"{part_stem} rendered at {n} pages")
        (BUNDLE / f"{part_stem}.md").write_text(note + text)
        written.append((part_stem, n))
    return written


def rows_from_pdf(page_indexes, x_stops):
    """Rebuild table rows from positioned text. A row is one visual line, not a wrapped paragraph."""
    reader = PdfReader(str(OLD_PDF))
    out = []
    for idx in page_indexes:
        items = []

        def visitor(text, cm, tm, fontDict, fontSize, _items=items):
            if text and text.strip():
                _items.append((round(tm[5], 1), round(tm[4], 1), text.replace("\n", "").strip()))

        reader.pages[idx].extract_text(visitor_text=visitor)
        buckets = defaultdict(list)
        for y, x, t in items:
            buckets[y].append((x, t))
        for y in sorted(buckets, reverse=True):
            cells = [""] * (len(x_stops) - 1)
            for x, t in sorted(buckets[y]):
                for k in range(len(x_stops) - 1):
                    if x_stops[k] <= x < x_stops[k + 1]:
                        cells[k] = (cells[k] + " " + t).strip()
                        break
            if any(cells):
                out.append(cells)
    return out


def md_table(headers, rows):
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(c.replace("|", "/") for c in r) + " |" for r in rows]
    return "\n".join([head, sep, *body])


def ascii_name(n: int) -> str:
    names = {
        0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK", 7: "BEL",
        8: "BS", 9: "HT", 10: "LF", 11: "VT", 12: "FF", 13: "CR", 14: "SO", 15: "SI",
        16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN", 23: "ETB",
        24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS", 30: "RS", 31: "US",
        32: "SP", 127: "DEL",
    }
    if n in names:
        return names[n]
    if 33 <= n <= 126:
        ch = chr(n)
        if ch == "|":
            return "vertical bar"
        return ch
    return ""


def strip_first_h1_keep(text: str) -> str:
    return text


CHAPTERS = [
    "00-how-to-read.md",
    "01-corpus.md",
    "02-formats.md",
    "03-runtime.md",
    "04-objects.md",
    "05-graphics.md",
    "06-openscript.md",
    "07-debugging.md",
    "08-naming.md",
    "09-modern.md",
    "10-open.md",
    "11-keepers.md",
    "12-wdw-spine.md",
    "13-specimen-pages.md",
    "14-openscript-bytes.md",
    "15-system-books.md",
    "16-cipher.md",
    "17-modules.md",
    "18-absorption.md",
    "19-heap-stack-resmgr.md",
    "20-cdb-obj.md",
    "21-stress.md",
    "22-value-vbx-execscript.md",
]


def first_heading(text: str, fallback: str) -> str:
    m = re.search(r"(?m)^# +(.+)$", text)
    return m.group(1).strip() if m else fallback


def pdf_parts(stem: str) -> list[tuple[str, int]]:
    exact = OUT_DIRS[0] / f"{stem}.pdf"
    if exact.is_file():
        return [(stem, len(PdfReader(str(exact)).pages))]
    parts = sorted(OUT_DIRS[0].glob(f"{stem}-*.pdf"))
    return [(path.stem, len(PdfReader(str(path)).pages)) for path in parts]


def pdf_pages(stem: str):
    parts = pdf_parts(stem)
    if len(parts) == 1 and parts[0][0] == stem:
        return parts[0][1]
    return None


def toc_markdown() -> str:
    """The interchangeable sheet. Chapter titles come from the record.

    Page counts come from PDFs already printed. A dash means that file
    has not been typeset. This function does not render the contents.
    """
    lines = [
        "# Table of contents",
        "",
        "**Date:** " + EDITION_DATE,
        "",
        "Print this sheet on its own. It is not inside the contents file. "
        "The chapter list is the record on disk. The page counts are the PDFs that already exist. "
        "If those two disagree, the record is ahead of the print, and this sheet is the one to replace.",
        "",
        "| Piece | File | Pages |",
        "| --- | --- | --- |",
    ]

    def row(piece, stem):
        parts = pdf_parts(stem)
        if not parts:
            lines.append(f"| {piece} | `{stem}.pdf` | — |")
            return
        for name, n in parts:
            label = piece if name == stem else f"{piece} ({name})"
            lines.append(f"| {label} | `{name}.pdf` | {n} |")

    row("Cover", "cover")
    row("Table of contents", "toc")
    row("Preface", "preface")
    row("Foreword", "foreword")
    row("Contents", "contents")
    lines += [
        "",
        "## Inside the contents",
        "",
        "These titles are the first heading of each file in `TBdecompile/record/`, in order. "
        "Their pages inside the contents file are not on this sheet. Counting those pages means typesetting the contents.",
        "",
    ]
    for name in CHAPTERS:
        title = first_heading((RECORD / name).read_text(), name)
        lines.append(f"- {title}")
    lines += ["", "## Appendices", "", "| Appendix | File | Pages |", "| --- | --- | --- |"]
    for stem, (_left, right) in HEADERS.items():
        if not stem.startswith("appendix-"):
            continue
        n = pdf_pages(stem)
        if n is None and pdf_parts(stem):
            n = sum(pages for _name, pages in pdf_parts(stem))
            lines.append(f"| {right} | `{stem}-*.pdf` | {n} |")
            continue
        lines.append(f"| {right} | `{stem}.pdf` | {n if n else '—'} |")
    lines.append("")
    return "\n".join(lines)


def assemble():
    BUNDLE.mkdir(parents=True, exist_ok=True)
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    chapters = []
    for name in CHAPTERS:
        chapters.append((RECORD / name).read_text().rstrip() + "\n")
    contents = "\n\n".join(chapters) + "\n"
    (BUNDLE / "contents.md").write_text(contents)

    exports = []
    exports.append(
        "# Appendix A — Export and Ordinal Maps\n\n"
        "BAS, RTM, and W16 exports, then the BAS ordinals that have been tied to a segment.\n\n"
        "**Date:** 16 October 2026\n\n"
        "These four tables are the 12 October map notes, copied whole. "
        "A row was not dropped to shorten the file, and the tables were not interleaved with the numeric tables or the address maps. "
        "Those are Appendix E and Appendix D.\n\n"
        "An address in this appendix is a location. It is not a claim about when the function runs. "
        "`CDBSENDCREATE` is in the BAS table because it is an export. "
        "It is the author create path. It is not the runtime reader. That correction is Appendix B and chapter 4 of the contents. "
        "The row itself is unchanged.\n\n"
    )
    for src, title in [
        (OLD_MAPS / "07-bas-export-map.md", "BAS export map"),
        (OLD_MAPS / "08-rtm-export-map.md", "RTM export map"),
        (OLD_MAPS / "09-w16-export-map.md", "W16 export map"),
        (OLD_MAPS / "10-bas-ordinal-map.md", "BAS ordinal map"),
    ]:
        body = src.read_text().rstrip()
        # The source files already have their own titles. Keep them.
        exports.append(body + "\n")
    (BUNDLE / "appendix-a-exports.md").write_text("\n\n".join(exports) + "\n")

    (BUNDLE / "appendix-b-architecture.md").write_text((SOURCES / "appendix-b-architecture.md").read_text())
    (BUNDLE / "appendix-c-tbx.md").write_text((SOURCES / "appendix-c-tbx.md").read_text())

    maps = []
    maps.append(
        "# Appendix D — Address Maps\n\n"
        "NE segment to Ghidra space, and one boot's WDW selectors.\n\n"
        "**Date:** 16 October 2026\n\n"
        "Each map below is the current file, complete. "
        "NE segment numbers are not Ghidra `CodeN` names. "
        "Segment 1 is `1000`, segment 2 is `1008`, and the usual step is 8, with gaps. "
        "Live selectors change every boot. Offsets inside a segment do not. "
        "The symbol maps are not reprinted. They are unsifted decompiler names and were removed from this edition. "
        "They remain on disk under `TBdecompile/trail/20261015/20261012/`. "
        "The Bochs selectors from 20 October are the last map. They die at the next reboot. "
        "Appendix L is the command card for that host.\n\n"
    )
    for src in [
        MAPS / "bas-ne-to-ghidra.md",
        MAPS / "rtm-ne-to-ghidra.md",
        MAPS / "wdw-to-ghidra.md",
        MAPS / "bochs-20261020.md",
    ]:
        maps.append(src.read_text().rstrip() + "\n")
    (BUNDLE / "appendix-d-maps.md").write_text("\n\n".join(maps) + "\n")

    # Appendix E — numeric tables. ASCII and decimal/hex are generated in full.
    # Win16 ordinals are lifted row by row from the 15 October appendix.
    win_rows = rows_from_pdf([14, 15, 16, 17], [0, 50, 100, 600])
    win_data = []
    for lib, ordinal, name in win_rows:
        if lib in ("Library",) or name in ("Name",) or "Win16" in lib or "Numbers restart" in lib:
            continue
        if not ordinal.isdigit():
            continue
        win_data.append((lib, ordinal, name))

    hex_rows = [(f"{n}", f"{n:02X}") for n in range(256)]
    # Four pairs across, so the table is complete and still a table.
    hex_lines = ["| Dec | Hex | Dec | Hex | Dec | Hex | Dec | Hex |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for base in range(0, 256, 4):
        cells = []
        for n in range(base, base + 4):
            cells.append(str(n))
            cells.append(f"{n:02X}")
        hex_lines.append("| " + " | ".join(cells) + " |")

    ascii_lines = ["| Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for base in range(0, 128, 4):
        cells = []
        for n in range(base, base + 4):
            cells.extend([str(n), f"{n:02X}", ascii_name(n)])
        ascii_lines.append("| " + " | ".join(cells) + " |")

    e = []
    e.append(
        "# Appendix E — Numeric and System Tables\n\n"
        "Decimal/hex, ASCII, and the Win16 ordinals used when a trace names KERNEL, USER, or GDI by number.\n\n"
        "**Date:** 16 October 2026\n\n"
        "Decimal/hex is 0 through 255. ASCII is 0 through 127. Neither table is cut off early. "
        "The Win16 rows are the 15 October appendix, in the same order, one ordinal per row. "
        "Numbers restart at 1 for each library.\n\n"
        "## Decimal to hexadecimal\n\n"
        + "\n".join(hex_lines)
        + "\n\n## ASCII (0–127)\n\n"
        "Controls are shown by name. The landscape one-page card remains `TBdecompile/ASCII_lookup.pdf`.\n\n"
        + "\n".join(ascii_lines)
        + "\n\n## Win16 system ordinals\n\n"
        + md_table(["Library", "Ordinal", "Name"], win_data)
        + "\n"
    )
    (BUNDLE / "appendix-e-tables.md").write_text("".join(e))

    name_rows = rows_from_pdf([18, 19, 20], [0, 40, 150, 600])
    name_data = []
    for mod, fn, name in name_rows:
        if mod in ("Module",) or fn in ("Function",) or "Confirmed" in mod:
            continue
        if not fn.startswith("FUN_") and not fn.startswith("Ordinal"):
            continue
        name_data.append((mod, fn, name))
    f = []
    f.append(
        "# Appendix F — Confirmed Function Names\n\n"
        "The rename table from the 15 October lookups, carried forward whole.\n\n"
        "**Date:** 16 October 2026\n\n"
        "A name in this table is the name attached in the decompile. "
        "It is not, by itself, a claim that the function runs on book open. "
        "Module roles are chapter 17 of the contents.\n\n"
        + md_table(["Module", "Function", "Name"], name_data)
        + "\n"
    )
    (BUNDLE / "appendix-f-names.md").write_text("".join(f))

    def load_appendix(src_name, bundle_name):
        body = (SOURCES / src_name).read_text()
        (BUNDLE / bundle_name).write_text(body)
        return body

    g = load_appendix("appendix-g-softice.md", "appendix-g-softice.md")
    h = load_appendix("appendix-h-watcom.md", "appendix-h-watcom.md")
    i = load_appendix("appendix-i-assembly.md", "appendix-i-assembly.md")
    j = load_appendix("appendix-j-openscript.md", "appendix-j-openscript.md")
    k = load_appendix("appendix-k-ghidra.md", "appendix-k-ghidra.md")
    l = load_appendix("appendix-l-bochs.md", "appendix-l-bochs.md")
    cover = (SOURCES / "front-cover.md").read_text()
    foreword = (SOURCES / "front-foreword.md").read_text()
    preface = (SOURCES / "front-preface.md").read_text()
    (BUNDLE / "cover.md").write_text(cover)
    (BUNDLE / "foreword.md").write_text(foreword)
    (BUNDLE / "preface.md").write_text(preface)
    return {
        "cover": cover,
        "foreword": foreword,
        "preface": preface,
        "contents": contents,
        "appendix-a-exports": (BUNDLE / "appendix-a-exports.md").read_text(),
        "appendix-b-architecture": (BUNDLE / "appendix-b-architecture.md").read_text(),
        "appendix-c-tbx": (BUNDLE / "appendix-c-tbx.md").read_text(),
        "appendix-d-maps": (BUNDLE / "appendix-d-maps.md").read_text(),
        "appendix-e-tables": (BUNDLE / "appendix-e-tables.md").read_text(),
        "appendix-f-names": (BUNDLE / "appendix-f-names.md").read_text(),
        "appendix-g-softice": g,
        "appendix-h-watcom": h,
        "appendix-i-assembly": i,
        "appendix-j-openscript": j,
        "appendix-k-ghidra": k,
        "appendix-l-bochs": l,
    }


HEADERS = {
    "cover": ("TBdecompile Reference Manual", "Cover"),
    "toc": ("TBdecompile Reference Manual", "Table of contents"),
    "preface": ("TBdecompile Reference Manual", "Preface"),
    "foreword": ("TBdecompile Reference Manual", "Foreword"),
    "contents": ("TBdecompile Reference Manual", "Contents"),
    "appendix-a-exports": ("TBdecompile Reference Manual", "Appendix A — Export and Ordinal Maps"),
    "appendix-b-architecture": ("TBdecompile Reference Manual", "Appendix B — Architecture and Gaps"),
    "appendix-c-tbx": ("TBdecompile Reference Manual", "Appendix C — TBX File Format"),
    "appendix-d-maps": ("TBdecompile Reference Manual", "Appendix D — Address Maps"),
    "appendix-e-tables": ("TBdecompile Reference Manual", "Appendix E — Numeric and System Tables"),
    "appendix-f-names": ("TBdecompile Reference Manual", "Appendix F — Confirmed Function Names"),
    "appendix-g-softice": ("TBdecompile Reference Manual", "Appendix G — SoftICE"),
    "appendix-h-watcom": ("TBdecompile Reference Manual", "Appendix H — The Watcom Debugger"),
    "appendix-i-assembly": ("TBdecompile Reference Manual", "Appendix I — Reading the Assembly"),
    "appendix-j-openscript": ("TBdecompile Reference Manual", "Appendix J — OpenScript"),
    "appendix-k-ghidra": ("TBdecompile Reference Manual", "Appendix K — Ghidra"),
    "appendix-l-bochs": ("TBdecompile Reference Manual", "Appendix L — Bochs"),
}


def copy_out(names=()):
    src_dir = OUT_DIRS[0]
    wanted = {f"{name}.pdf" for name, _n in names}
    for dest_root in OUT_DIRS[1:]:
        dest_root.mkdir(parents=True, exist_ok=True)
        paths = {p.name: p for p in src_dir.glob("*.pdf")}
        for name in wanted:
            paths[name] = src_dir / name
        for name, path in paths.items():
            if path.is_file():
                (dest_root / name).write_bytes(path.read_bytes())


def render_one(stem: str, md: str) -> list[tuple[str, int]]:
    left, right = HEADERS[stem]
    if stem == "cover":
        n = render(md, OUT_DIRS[0] / "cover.pdf", left, right, bare=True)
        if n >= PAGE_CAP:
            raise SystemExit(f"cover rendered at {n} pages")
        return [("cover", n)]
    return pack(md, stem, left, right)


def write_toc() -> str:
    text = toc_markdown()
    (BUNDLE / "toc.md").write_text(text)
    return text


def merge_single(order: list[str]) -> int:
    """The separate sheets, in reading order, as one PDF. Page numbers stay the sheet's own."""
    writer = PdfWriter()
    for stem in order:
        for name, _n in pdf_parts(stem):
            reader = PdfReader(str(EDITION / f"{name}.pdf"))
            for page in reader.pages:
                writer.add_page(page)
    dest = EDITION / SINGLE
    with dest.open("wb") as handle:
        writer.write(handle)
    return len(PdfReader(str(dest)).pages)


def main():
    import sys

    docs = assemble()
    only_front = len(sys.argv) > 1 and sys.argv[1] == "front"
    results = []
    order = ["cover", "preface", "foreword"]
    if not only_front:
        order += [stem for stem in docs if stem not in ("cover", "preface", "foreword")]
    for stem in order:
        results.extend(render_one(stem, docs[stem]))
        print(f"{stem}: " + ", ".join(f"{name}={n}p" for name, n in results[-1:]))
    # The contents sheet is last so its page column can see the files just written.
    toc = write_toc()
    results.extend(render_one("toc", toc))
    print("toc: " + ", ".join(f"{name}={n}p" for name, n in results[-1:]))
    copy_out(results)
    reading = ["cover", "toc", "preface", "foreword"]
    if not only_front:
        reading += [stem for stem in docs if stem not in ("cover", "preface", "foreword")]
    single_pages = merge_single(reading)
    print(f"single: {SINGLE}={single_pages}p")
    lines = [
        f"# {EDITION_DATE} edition",
        "",
        f"`{SINGLE}` is the whole book: cover, table of contents, preface, foreword, contents, then appendices A through L.",
        "The other files are the same book in parts. Front matter is four files. Each part is under 100 pages.",
        "Breaks, where a file was split, fall between headings.",
        "",
        "| File | Pages |",
        "| --- | --- |",
        f"| `{SINGLE}` | {single_pages} |",
    ]
    # List the sheets in reading order, not the order they were typeset.
    shown = {SINGLE}
    for stem in reading:
        for name, n in pdf_parts(stem):
            if name in shown:
                continue
            lines.append(f"| `{name}.pdf` | {n} |")
            shown.add(name)
    lines.append("")
    lines.append("Source for the contents is `record/`. Appendix prose is `manual/sources/`. The generated sheets' markdown is `src/`.")
    lines.append("")
    manifest = "\n".join(lines)
    (BUNDLE / "MANIFEST.md").write_text(manifest)
    (EDITION / "README.md").write_text(manifest)
    print("done")
    for name, n in results:
        if n >= PAGE_CAP:
            raise SystemExit(f"cap exceeded: {name} {n}")
    if single_pages < 1:
        raise SystemExit("the single PDF is empty")


if __name__ == "__main__":
    main()
