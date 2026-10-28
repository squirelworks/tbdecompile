"""Play a ToolBook II 8.1 course book.

Writes a self-contained HTML reader: page text, Next, Back, and the
quoted page jumps the handlers push. Does not execute OpenScript.

  python -m runtime courses/93955601.tbk
  python -m runtime courses/93955601.tbk --out /tmp/lesson.html
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .play import write
from .tbk import load


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Play a ToolBook II 8.1 course book")
    p.add_argument("book")
    p.add_argument("--out", help="HTML reader path (default: runtime/out/<book>.html)")
    args = p.parse_args(argv)
    book = load(args.book)
    if not book.pages:
        print(f"{book.path.name}: no pages", file=sys.stderr)
        return 1
    dest = Path(args.out) if args.out else Path(__file__).resolve().parent / "out" / f"{book.path.stem}.html"
    write(book, dest)
    with_text = sum(1 for page in book.pages if page.fields or page.paragraphs)
    with_jumps = sum(1 for page in book.pages if page.quoted_jumps)
    print(f"{book.path.name}: {len(book.pages)} pages, {with_text} with text, {with_jumps} with jumps")
    print(f"reader: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
