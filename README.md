# TBDecompile

ToolBook II 8.1 decompilation notes. Release **v0.0.2** (16 October 2026). The current statement is [`record/`](record/00-how-to-read.md). The printable copy of the record is [`record/ToolBook-record-20261016.pdf`](record/ToolBook-record-20261016.pdf). The reference-manual edition that sets that record as the contents, and keeps the lookups in their own files, is [`manual/20261016/`](manual/20261016/README.md). The 15 October contents and appendix PDFs are in [`editions/v0.0.1/`](editions/v0.0.1). They are not current where they put `CDBSENDCREATE` on book open.

Loose sheets under `tbworkingpapers/` are the trail. [`record/18-absorption.md`](record/18-absorption.md) names each one and the section that replaced it. When they disagree with `record/`, `record/` wins.

## Contents

- `record/` — the official volume: corpus, formats, runtime, objects, graphics, OpenScript, debugging, naming, the modern stack, open questions, keepers, the WDW spine, specimen pages, bytecode, system books, the password cipher, modules, and the absorption index
- `trail/20261016/` — the short correction this volume expands
- `trail/20261015/` — how ToolBook operates. Section 2 of the operating note is superseded (author path, not runtime)
- `trail/20261014/` — the working papers, condensed. The opening of `02-still-open.md` is superseded
- `trail/20261012/` — the earlier consolidation
- `maps/` — NE segment to Ghidra, and one boot's WDW selectors. Lookups, not a narrative
- `rename/` — Ghidra rename scripts and the nameable lists
- `editions/v0.0.1/` — the previous printable edition

`nehost` is not in this repository. The host and the pass logs are `tbpipeline/tbpipeline_bf/nehost/`.

## Status

The record reader is still unnamed. `CDBSENDCREATE` (BAS ordinal 51) is author-only and is not on the runtime path. Content rectangles and the kind-`0400` polygon record are decoded. Curves, arcs, and picture placement are not. TBCBT NE segment 7 holds the password cipher. The live key has not been captured.

Binary dumps stay out of this repository. Personal names stay out. The correspondent is JohnDoe1.
