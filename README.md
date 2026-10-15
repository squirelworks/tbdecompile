# TBDecompile

ToolBook II 8.1 decompilation notes. The current statement is [`record/`](record/00-how-to-read.md). The printable copy is [`record/ToolBook-record-20261016.pdf`](record/ToolBook-record-20261016.pdf).

Loose sheets under `tbworkingpapers/` are the trail. [`record/18-absorption.md`](record/18-absorption.md) names each one and the section that replaced it. When they disagree with `record/`, `record/` wins.

## Contents

- `record/` — the official volume: corpus, formats, runtime, objects, graphics, OpenScript, debugging, naming, the modern stack, open questions, keepers, the WDW spine, specimen pages, bytecode, system books, the password cipher, modules, and the absorption index
- `20261016/` — the short correction this volume expands
- `20261015/` — how ToolBook operates. Section 2 of the operating note is superseded (author path, not runtime)
- `20261014/` — the working papers, condensed. The opening of `02-still-open.md` is superseded
- `20261012/` — the earlier consolidation
- `maps/` — NE segment to Ghidra, and one boot's WDW selectors. Lookups, not a narrative
- `rename/` — Ghidra rename scripts and the nameable lists
- `nehost/` — Unicorn and load-sequence experiments. Local only unless a commit names it

## Status

The record reader is still unnamed. `CDBSENDCREATE` (BAS ordinal 51) is author-only and is not on the runtime path. Content rectangles and the kind-`0400` polygon record are decoded. Curves, arcs, and picture placement are not. TBCBT NE segment 7 holds the password cipher. The live key has not been captured.

Binary dumps stay out of this repository. Personal names stay out. The correspondent is JohnDoe1.
