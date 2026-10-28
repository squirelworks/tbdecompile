"""Standard property ids from TB80BAS resource type 0x2d1 id 0x2d0.

Id is 0x4000 + slot. Filled at runtime by FUN_1290_000e into DAT_1630_19fa.
This table is the name list only. Getters still live in the old BAS segments.
"""

from __future__ import annotations

from pathlib import Path

PROPS: dict[int, str] = {}
NAMES: dict[str, int] = {}


def load(path: str | Path | None = None) -> dict[int, str]:
    if path is None:
        path = Path(__file__).resolve().parents[1] / "viewer2" / "stdprops.tsv"
    path = Path(path)
    PROPS.clear()
    NAMES.clear()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("id"):
            continue
        ident, name = line.split("\t", 1)
        pid = int(ident, 16)
        PROPS[pid] = name
        NAMES[name] = pid
    return PROPS


# Properties the course books actually exercise first.
BOUNDS = 0x4004
CAPTION = 0x4005
ID_NUMBER = 0x4015
NAME = 0x401B
PAGE_COUNT = 0x401E
SCRIPT = 0x4023
TEXT = 0x402E
VERTICES = 0x4034
