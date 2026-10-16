# TBDecompile

ToolBook II 8.1 decompilation notes. Release **v0.0.8** (16 October 2026). The current statement is [`record/`](record/00-how-to-read.md). The printable copy is [`manual/20261016/`](manual/20261016/README.md): cover, table of contents, preface, and foreword are separate files, then the contents, then appendices A through K. Appendix K is how to disassemble. `toc.pdf` is the sheet reprinted on its own. Chapter 13 now says where P440's text sits. Chapter 22 is the value bus, VBX, and `EXECSCRIPT`. The 15 October contents and appendix PDFs are in [`editions/v0.0.1/`](editions/v0.0.1). They are not current where they put `CDBSENDCREATE` on book open.

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
