"""TBX OpenScript engine.

Loads a SumTotal ToolBook TBKX export folder and interprets the plain-text
.script files that accompany Book.xml / Page.xml / Background.xml.

Supported constructs (matching the Nida lesson corpus):
  to handle NAME ... end
  go to page "P" [of book "B"]
  send NAME
  NAME = EXPR
  put EXPR into NAME
  set PROP of TARGET to EXPR
  get EXPR
  increment / decrement NAME
  if / else / end if (nested)
  conditions / when / else / end conditions
  step NAME from A to B
  name of this book / name of this page
  system declarations (ignored)
  forward / break
  simple function calls (get name(...), isObject(...))

Returns a list of actions the host can apply. Does not claim to be a full
OpenScript implementation; it covers the subset used by the exported books.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

@dataclass
class TbxObject:
    kind: str
    id_number: str
    name: str
    script_file: str | None = None
    bounds: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class TbxPage:
    id_number: str
    name: str
    background: str = ""
    script_file: str | None = None
    objects: list[TbxObject] = field(default_factory=list)
    user_props: dict = field(default_factory=dict)


@dataclass
class TbxBook:
    path: Path
    caption: str = ""
    size: str = ""
    book_script: str | None = None
    pages: dict[str, TbxPage] = field(default_factory=dict)   # by name
    backgrounds: dict[str, TbxPage] = field(default_factory=dict)
    scripts: dict[str, str] = field(default_factory=dict)     # relative path -> text


@dataclass
class RuntimeState:
    book: TbxBook
    current_page: str = ""
    variables: dict[str, Any] = field(default_factory=dict)
    sys_level: str = "reader"
    sys_books: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

NS = {"tb": "urn:sumtotalsystems:toolbook.tbkx"}


def load_tbx(folder: str | Path) -> TbxBook:
    """Load a TBKX export folder into a TbxBook."""
    root = Path(folder)
    if not root.is_dir():
        raise FileNotFoundError(folder)

    book = TbxBook(path=root)

    # Book.xml
    book_xml = root / "Book.xml"
    if book_xml.exists():
        tree = ET.parse(book_xml)
        el = tree.getroot()
        book.caption = el.get("Caption", "")
        book.size = el.get("Size", "")
        script = el.get("Script")
        if script:
            book.book_script = script
            p = root / script
            if p.exists():
                book.scripts[script] = p.read_text(encoding="utf-8", errors="replace")

    # Pages
    for page_dir in sorted(root.glob("Page*")):
        xml = page_dir / "Page.xml"
        if not xml.exists():
            continue
        page = _load_page_or_bg(xml, page_dir, root, book)
        if page and page.name:
            book.pages[page.name] = page

    # Backgrounds
    for bg_dir in sorted(root.glob("Background*")):
        xml = bg_dir / "Background.xml"
        if not xml.exists():
            continue
        bg = _load_page_or_bg(xml, bg_dir, root, book)
        if bg:
            key = bg.name or bg.id_number
            book.backgrounds[key] = bg

    return book


def _load_page_or_bg(xml_path: Path, directory: Path, root: Path, book: TbxBook) -> TbxPage | None:
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        return None
    el = tree.getroot()
    page = TbxPage(
        id_number=el.get("IdNumber", ""),
        name=el.get("Name", ""),
        background=el.get("Background", ""),
    )
    # page-level script is usually external; look for matching .script in the folder
    for script in directory.glob("*.script"):
        rel = str(script.relative_to(root))
        book.scripts[rel] = script.read_text(encoding="utf-8", errors="replace")
        # simple heuristic: first script that looks like a page handler
        if page.script_file is None:
            page.script_file = rel

    # objects: only direct graphic/widget tags that carry an IdNumber
    for obj_el in el.iter():
        if not obj_el.get("IdNumber"):
            continue
        tag = obj_el.tag.split("}")[-1]
        if tag in ("Page", "Background", "UserProperty"):
            continue
        obj = TbxObject(
            kind=tag,
            id_number=obj_el.get("IdNumber", ""),
            name=obj_el.get("Name", ""),
            bounds=obj_el.get("Bounds", "") or obj_el.get("Vertices", ""),
        )
        # matching script file, if any
        script_path = directory / f"{tag}{obj.id_number}.script"
        if script_path.exists():
            rel = str(script_path.relative_to(root))
            book.scripts[rel] = script_path.read_text(encoding="utf-8", errors="replace")
            obj.script_file = rel
        page.objects.append(obj)

    # user properties
    for up in el.findall(".//UserProperty"):
        page.user_props[up.get("Name", "")] = up.get("Value", "")

    return page


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------

_GOTO = re.compile(r'go\s+to\s+page\s+"([^"]+)"(?:\s+of\s+book\s+"([^"]+)")?', re.I)
_SEND = re.compile(r'send\s+(\w+)', re.I)
_PUT = re.compile(r'put\s+(.+?)\s+into\s+(\w+)', re.I)
_SET = re.compile(r'set\s+(.+?)\s+to\s+(.+)', re.I)
_GET = re.compile(r'get\s+(.+)', re.I)
_STEP = re.compile(r'step\s+(\w+)\s+from\s+(.+?)\s+to\s+(.+?)(?:\s+by\s+(.+))?$', re.I)
_INC = re.compile(r'(increment|decrement)\s+(\w+)', re.I)
_ASSIGN = re.compile(r'(\w+)\s*=\s*(.+)')
_NAME_OF = re.compile(r'name\s+of\s+this\s+(book|page)', re.I)
_WHEN = re.compile(r'when\s+(.+)', re.I)


def run_script(state: RuntimeState, source: str) -> list[dict]:
    """Execute one handler source. Returns the list of actions produced."""
    actions: list[dict] = []
    if not source:
        return actions
    lines = _normalize(source)
    _run_block(state, lines, 0, len(lines), actions)
    return actions


def run_page_enter(state: RuntimeState, page_name: str) -> list[dict]:
    """Run the enterPage handler(s) for a named page (page script + background)."""
    state.current_page = page_name
    actions: list[dict] = []
    page = state.book.pages.get(page_name)
    if not page:
        return actions
    # background first
    if page.background:
        bg_key = page.background.replace("Background id ", "").strip()
        # try by name or id
        for bg in state.book.backgrounds.values():
            if bg.id_number == bg_key or bg.name == page.background:
                if bg.script_file and bg.script_file in state.book.scripts:
                    actions.extend(run_script(state, state.book.scripts[bg.script_file]))
                break
    # page script
    if page.script_file and page.script_file in state.book.scripts:
        actions.extend(run_script(state, state.book.scripts[page.script_file]))
    return actions


def _normalize(source: str) -> list[str]:
    out = []
    for raw in source.replace("\r", "").split("\n"):
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        low = line.lower()
        if low.startswith("to handle"):
            continue
        if low in ("end", "end handler"):
            break
        out.append(line)
    return out


def _run_block(state: RuntimeState, lines: list[str], start: int, end: int, actions: list[dict]) -> int:
    i = start
    while i < end:
        line = lines[i]
        low = line.lower()

        # if / else / end if
        if low.startswith("if ") and " then" in low:
            cond = line[3:low.rfind(" then")].strip()
            body_start = i + 1
            else_at, end_at = _split_if(lines, body_start, end)
            if _truth(_eval(cond, state)):
                _run_block(state, lines, body_start, else_at, actions)
            elif else_at < end_at:
                _run_block(state, lines, else_at + 1, end_at, actions)
            i = end_at + 1
            continue

        # conditions / when / else / end conditions
        if low.startswith("conditions"):
            body_start = i + 1
            end_at = _find_end(lines, body_start, end, "end conditions")
            _run_conditions(state, lines, body_start, end_at, actions)
            i = end_at + 1
            continue

        # step
        if low.startswith("step "):
            m = _STEP.match(line)
            if m:
                name, a, b, by = m.group(1), m.group(2), m.group(3), m.group(4)
                body_start = i + 1
                end_at = _find_end(lines, body_start, end, "end step")
                _run_step(state, name, a, b, by, lines, body_start, end_at, actions)
                i = end_at + 1
                continue

        if low.startswith("system "):
            i += 1
            continue
        if low in ("forward", "break"):
            actions.append({"kind": low})
            i += 1
            continue

        m = _GOTO.search(line)
        if m:
            actions.append({"kind": "goto", "page": m.group(1), "book": m.group(2)})
            i += 1
            continue
        m = _SEND.search(line)
        if m:
            actions.append({"kind": "send", "name": m.group(1)})
            i += 1
            continue
        m = _PUT.match(line)
        if m:
            value = _eval(m.group(1), state)
            state.variables[m.group(2)] = value
            actions.append({"kind": "set", "name": m.group(2), "value": value})
            i += 1
            continue
        m = _SET.match(line)
        if m:
            value = _eval(m.group(2), state)
            actions.append({"kind": "setprop", "target": m.group(1).strip(), "value": value})
            i += 1
            continue
        m = _GET.match(line)
        if m:
            value = _eval(m.group(1), state)
            actions.append({"kind": "get", "expr": m.group(1).strip(), "value": value})
            i += 1
            continue
        m = _INC.match(line)
        if m:
            name = m.group(2)
            cur = state.variables.get(name, 0)
            try:
                cur = int(cur)
            except (TypeError, ValueError):
                cur = 0
            cur = cur + 1 if m.group(1).lower() == "increment" else cur - 1
            state.variables[name] = cur
            actions.append({"kind": "set", "name": name, "value": cur})
            i += 1
            continue
        m = _ASSIGN.match(line)
        if m and not low.startswith("if "):
            name, expr = m.group(1), m.group(2)
            value = _eval(expr, state)
            state.variables[name] = value
            actions.append({"kind": "set", "name": name, "value": value})
            i += 1
            continue

        actions.append({"kind": "note", "text": line})
        i += 1
    return i


def _split_if(lines: list[str], start: int, end: int) -> tuple[int, int]:
    depth = 1
    else_at = end
    for i in range(start, end):
        low = lines[i].lower()
        if low.startswith("if ") and " then" in low:
            depth += 1
        elif low.startswith("else") and depth == 1 and else_at == end:
            else_at = i
        elif low.startswith("end if"):
            depth -= 1
            if depth == 0:
                return (else_at if else_at < i else i), i
    return end, end


def _find_end(lines: list[str], start: int, end: int, marker: str) -> int:
    depth = 1
    for i in range(start, end):
        low = lines[i].lower()
        if low.startswith(marker.split()[0]) and marker.split()[0] != "end":
            # crude: only count matching openers for step/conditions
            if marker == "end step" and low.startswith("step "):
                depth += 1
            elif marker == "end conditions" and low.startswith("conditions"):
                depth += 1
        if low.startswith(marker):
            depth -= 1
            if depth == 0:
                return i
    return end


def _run_conditions(state, lines, start, end, actions):
    # simple linear scan for the first true when, else fall-through
    i = start
    taken = False
    while i < end:
        low = lines[i].lower()
        if low.startswith("when "):
            cond = lines[i][5:].strip()
            body_start = i + 1
            next_when = end
            for j in range(body_start, end):
                if lines[j].lower().startswith("when ") or lines[j].lower().startswith("else"):
                    next_when = j
                    break
            if not taken and _truth(_eval(cond, state)):
                _run_block(state, lines, body_start, next_when, actions)
                taken = True
            i = next_when
            continue
        if low.startswith("else") and not taken:
            _run_block(state, lines, i + 1, end, actions)
            taken = True
            break
        i += 1


def _run_step(state, name, a, b, by, lines, start, end, actions):
    try:
        lo = int(_eval(a, state))
        hi = int(_eval(b, state))
        step = int(_eval(by, state)) if by else 1
    except (TypeError, ValueError):
        actions.append({"kind": "note", "text": f"step {name} not numeric"})
        return
    if step == 0:
        return
    cur = lo
    guard = 0
    while (cur <= hi if step > 0 else cur >= hi) and guard < 10000:
        state.variables[name] = cur
        _run_block(state, lines, start, end, actions)
        cur += step
        guard += 1


def _eval(expr: str, state: RuntimeState) -> Any:
    expr = expr.strip().rstrip(".")
    if not expr:
        return ""
    low = expr.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    m = _NAME_OF.fullmatch(expr)
    if m:
        if m.group(1).lower() == "book":
            return state.book.caption or str(state.book.path.name)
        return state.current_page
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    if re.fullmatch(r"-?\d+", expr):
        return int(expr)
    # simple && concat
    if " && " in expr:
        parts = [str(_eval(p, state)) for p in expr.split(" && ")]
        return "".join(parts)
    # variable lookup
    if re.fullmatch(r"[A-Za-z_]\w*", expr):
        return state.variables.get(expr, expr)
    # isObject(...) stub
    if low.startswith("isobject("):
        return True
    # get-style call stub
    if re.match(r"^\w+\(", low):
        return None
    return expr


def _truth(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v is None or v == "" or v == 0 or v == "false":
        return False
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description="TBX OpenScript engine")
    ap.add_argument("tbx", help="Path to TBKX export folder")
    ap.add_argument("--page", help="Page name to enter (e.g. P900)")
    ap.add_argument("--script", help="Run a specific .script file relative to the TBX")
    ap.add_argument("--list", action="store_true", help="List pages and scripts")
    args = ap.parse_args()

    book = load_tbx(args.tbx)
    print(f"Loaded: {book.caption}  pages={len(book.pages)}  backgrounds={len(book.backgrounds)}  scripts={len(book.scripts)}")

    if args.list:
        for name in sorted(book.pages):
            p = book.pages[name]
            print(f"  {name:12}  id={p.id_number:6}  objects={len(p.objects):3}  script={p.script_file or '-'}")
        return

    state = RuntimeState(book=book)
    if args.page:
        actions = run_page_enter(state, args.page)
        print(json.dumps(actions, indent=2, default=str))
    elif args.script:
        src = book.scripts.get(args.script)
        if not src:
            print(f"script not found: {args.script}")
            return
        actions = run_script(state, src)
        print(json.dumps(actions, indent=2, default=str))
    else:
        print("Use --page P900 or --script Book.script or --list")


if __name__ == "__main__":
    main()
