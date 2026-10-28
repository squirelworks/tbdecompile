"""Documenter. You name the directory. It does not pick a tree.

Walks that directory for .tbk files, runs the runtime reader on each one,
and writes a viewer3 catalog plus one HTML book per file.

  python -m runtime.documenter D:\\your\\tbk\\tree --xml courses.xml --out documented

courses.xml is optional. With it, the catalog is menu 0_MASTER3, the same
list as viewer2. Without it, every book found is one flat module.
A TBK that is not in the menu is still written and listed under "On disk".
"""

from __future__ import annotations

import argparse
import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from .play import render
from .tbk import load


def find_tbks(directory: Path) -> dict[str, Path]:
    found = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".tbk":
            found.setdefault(path.stem.lower(), path)
    return found


def master_menu(courses_xml: Path):
    root = ET.parse(courses_xml).getroot()
    for child in root.findall("Menu"):
        if child.get("courseid") == "0_MASTER3":
            return child
    raise SystemExit(f"no Menu courseid=0_MASTER3 in {courses_xml}")


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def write_viewer3(menu, written: dict[str, dict], dest: Path) -> None:
    """viewer3 extra.xml shape. file= is the runtime HTML, not a book xml."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<catalog title="Viewer3">',
    ]
    known = set()
    if menu is not None:
        for i, main in enumerate(menu.findall("Menu")):
            lines.append(f'  <main id="m{i}" title="{esc(main.get("title") or "")}">')
            for j, sub in enumerate(main.findall("Menu")):
                lines.append(f'    <sub id="m{i}s{j}" title="{esc(sub.get("title") or "")}">')
                for item in sub.findall("Item"):
                    lesson = item.get("lessonid") or ""
                    known.add(lesson.lower())
                    info = written.get(lesson.lower())
                    if not info:
                        continue
                    lines.append(
                        f'      <course id="{esc(info["id"])}" title="{esc(item.get("title") or lesson)}" '
                        f'file="books/{esc(info["id"])}.html"/>'
                    )
                lines.append("    </sub>")
            lines.append("  </main>")
    extra = [stem for stem in sorted(written) if stem not in known]
    if extra:
        lines.append('  <main id="disk" title="On disk">')
        lines.append('    <sub id="disks0" title="Not in courses.xml">')
        for stem in extra:
            info = written[stem]
            lines.append(
                f'      <course id="{esc(info["id"])}" title="{esc(info["id"])}" '
                f'file="books/{esc(info["id"])}.html"/>'
            )
        lines.append("    </sub>")
        lines.append("  </main>")
    lines.append("</catalog>")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(menu, written: dict[str, dict], dest: Path) -> None:
    parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">",
        "<title>Viewer3</title>",
        "<style>",
        "body{margin:0;background:#1c2430;color:#e8eef6;font:15px/1.4 system-ui,sans-serif}",
        "header{background:#1e4d8c;padding:14px 20px} main{max-width:880px;margin:0 auto;padding:16px 20px 40px}",
        "h2{font-size:18px;margin:22px 0 8px} h3{font-size:14px;color:#9eb4cc;margin:14px 0 4px}",
        "a{color:#d6e6f5;text-decoration:none} li{margin:3px 0} .meta{color:#9eb4cc;font-size:13px}",
        "</style></head><body><header><b>Viewer3</b>",
        "<div class=\"meta\">Runtime HTML for each book. Catalog is courses.xml menu 0_MASTER3.</div>",
        "</header><main>",
    ]
    known = set()
    if menu is not None:
        for main in menu.findall("Menu"):
            parts.append(f"<h2>{html.escape(main.get('title') or '')}</h2>")
            for sub in main.findall("Menu"):
                parts.append(f"<h3>{html.escape(sub.get('title') or '')}</h3><ul>")
                for item in sub.findall("Item"):
                    lesson = item.get("lessonid") or ""
                    known.add(lesson.lower())
                    info = written.get(lesson.lower())
                    title = html.escape(item.get("title") or lesson)
                    if info:
                        parts.append(
                            f"<li><a href=\"books/{html.escape(info['id'])}.html\">{title}</a> "
                            f"<span class=\"meta\">{html.escape(info['id'])} · {info['pages']} pages</span></li>"
                        )
                    else:
                        parts.append(f"<li class=\"meta\">{title} · {html.escape(lesson)} · no TBK</li>")
                parts.append("</ul>")
    extra = [stem for stem in sorted(written) if stem not in known]
    if extra:
        parts.append(f"<h2>On disk ({len(extra)})</h2><ul>")
        for stem in extra:
            info = written[stem]
            parts.append(
                f"<li><a href=\"books/{html.escape(info['id'])}.html\">{html.escape(info['id'])}</a> "
                f"<span class=\"meta\">{info['pages']} pages</span></li>"
            )
        parts.append("</ul>")
    parts.append(f"<p class=\"meta\">{len(written)} readers.</p></main></body></html>")
    dest.write_text("\n".join(parts), encoding="utf-8")


def document(tbk_dir: Path, courses_xml: Path | None, out: Path) -> int:
    if not tbk_dir.is_dir():
        print(f"not a directory: {tbk_dir}", file=sys.stderr)
        return 1
    books = find_tbks(tbk_dir)
    print(f"{len(books)} TBK files under {tbk_dir}")
    menu = master_menu(courses_xml) if courses_xml else None
    book_dir = out / "books"
    book_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, dict] = {}
    failed = 0
    paths = list(books.values())
    for n, path in enumerate(paths, 1):
        try:
            book = load(path)
            (book_dir / f"{path.stem}.html").write_text(render(book), encoding="utf-8")
        except Exception as exc:
            failed += 1
            print(f"fail {path}: {exc}", file=sys.stderr)
            continue
        written[path.stem.lower()] = {"id": path.stem, "pages": len(book.pages)}
        print(f"{n}/{len(paths)} {path.name} {len(book.pages)} pages", flush=True)
    write_viewer3(menu, written, out / "extra.xml")
    write_index(menu, written, out / "index.html")
    print(f"viewer3 catalog: {out / 'extra.xml'}")
    print(f"open: {out / 'index.html'}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run the runtime on each TBK in a directory you name")
    p.add_argument("tbk_dir", type=Path, help="your directory of .tbk files")
    p.add_argument("--xml", type=Path, help="courses.xml, menu 0_MASTER3")
    p.add_argument("--out", type=Path, default=Path("documented"), help="output directory")
    args = p.parse_args(argv)
    return document(args.tbk_dir, args.xml, args.out)


if __name__ == "__main__":
    sys.exit(main())
