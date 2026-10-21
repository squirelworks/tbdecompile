# TBDecompile

ToolBook II 8.1 decompilation notes. Release **v0.0.10r3** (22 October 2026). The current statement is [`record/`](record/00-how-to-read.md). The printable copy is [`manual/20261016/`](manual/20261016/README.md): cover, table of contents, preface, and foreword are separate files, then the contents, then appendices A through L. Appendix K is how to disassemble. Appendix L is the Bochs card. `toc.pdf` is the sheet reprinted on its own. Chapter 16.5 is the author session in which `ssssssssssss.tbk` became password-protected and `TBCBT` did not load. Chapter 13 says where P440's text sits. Chapter 22 is the value bus, VBX, and `EXECSCRIPT`. The 15 October contents and appendix PDFs are in [`editions/v0.0.1/`](editions/v0.0.1). They are not current where they put `CDBSENDCREATE` on book open.

Loose sheets under `tbworkingpapers/` are the trail. [`record/18-absorption.md`](record/18-absorption.md) names each one and the section that replaced it. When they disagree with `record/`, `record/` wins.

## Contents

- `record/` — the official volume: corpus, formats, runtime, objects, graphics, OpenScript, debugging, naming, the modern stack, open questions, keepers, the WDW spine, specimen pages, bytecode, system books, the password cipher, modules, and the absorption index
- `trail/20261016/` — the short correction this volume expands
- `trail/20261015/` — how ToolBook operates. Section 2 of the operating note is superseded (author path, not runtime)
- `trail/20261014/` — the working papers, condensed. The opening of `02-still-open.md` is superseded
- `trail/20261012/` — the earlier consolidation
- `maps/` — NE segment to Ghidra, one WDW boot, and the Bochs boot of 2026-10-20. Lookups, not a narrative.
- `rename/` — Ghidra rename scripts and the nameable lists
- `repair/` — how a bad listing was repaired, and the script that held. Not a second record.
- `research/` — short notes that are not a second record. The 21 October notes are the field text handle, the class table, class providers, and the paint offsets.
- `editions/v0.0.1/` — the previous printable edition

`nehost` is not in this repository. The host and the pass logs are `tbpipeline/tbpipeline_bf/nehost/`.

## Status

The record reader is the chain in chapter 4.6. `CDBSENDCREATE` (BAS ordinal 51) is author-only and is not on that path. On `9e954d01.tbk` the page list is book `+0x10` and all 131 page backgrounds resolve (`research/store-20261022.md`). A field is class `0xA` and its text is a trailer handle. A class `0x10` outline is not inline. A bitmap id is the fourth word of the directory entry. Neither lesson book stores a password block. TBCBT NE segment 7 still holds the empty-key cipher. The keyed 10-byte key has not been captured.

A field's text handle is word 1 of the block at object `+0x24`, not object `+0x42`. Segment 1278 loads class providers, not `sysBooks`. Class `0x3A` is the book's `ClassTbl`, and class `0x26` is `Viewer`. Those three notes are under `research/`.

Binary dumps stay out of this repository. Personal names stay out. The correspondent is JohnDoe1.
