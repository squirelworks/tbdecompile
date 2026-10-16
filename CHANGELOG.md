# Changelog

## v0.0.8r1 — 2026-10-17

- An author password on `ssssssssssss.tbk` did not load `TBCBT`. `nc81base.sbk` was refused and did not open. Chapter 16.5.
- The printable parts are the release assets. v0.0.8 tagged the edition and uploaded no PDFs.

## v0.0.8 — 2026-10-16

- P440 has no page record of its own. The sentence and the house shapes that overlap its TBX bounds are inside the P430 record. P2920 was not searched the same way.
- Foolbook 1.0.2 places shapes with `(coord * dpi + 720) / 1440`. Twip `0, 0` is the window origin.

## v0.0.7 — 2026-10-16

- Chapter 22. The value bus, a VBX control, and `EXECSCRIPT` are three mechanisms. None of them is the `0x76` page object.

## v0.0.6 — 2026-10-16

- Appendix K is the how-to-disassemble appendix: the work list, the two forced passes, and the difference between a name, a purpose, and an operation.

## v0.0.5 — 2026-10-16

- Chapter 21 records the stress run. Nested `step` and `if` now share a budget. A freed value is not the block that reused its index. Quotes are not split on `and`. Decoder output stops at its cap.

## v0.0.4 — 2026-10-16

- Appendix K is how Ghidra is used on these images, and how a listing is cleaned up over later passes. It does not name the record reader.
- The cover, the table of contents, the preface, and the foreword are separate files. `python3 build.py front` reprints those sheets, including `toc.pdf`, without typesetting the contents.
- The contents file is the record only. It is 49 pages and includes chapters 19 and 20. The earlier single-file PDF still ends at chapter 18.

## v0.0.2 — 2026-10-16

The statement is `record/`. The printable edition is `manual/20261016/`. v0.0.1's contents still put `CDBSENDCREATE` on book open. That placement is not in this release.

- `record/` consolidates the working papers. Chapters 11–18 add keepers, the WDW spine, specimen pages, the OpenScript encoding, system-book tiers, the TBCBT cipher, the module list, and the absorption index
- The reference manual is one contents volume (41 pages) and appendices A–J, each under 100 pages. Appendix J is OpenScript. The symbol-map dumps are not reprinted
- Author-path dispatch and the registrar's property ids are stated as author-only. Ordinal 51 is not the reader
- Graphic property names `0x4097`–`0x409B` are named. The page-blob slot is still open
- `nehost/` stays local. Binary dumps stay out

## 2026-10-16 — record

The loose working papers are consolidated into `record/`. That directory is the statement. The dated folders remain as the notes of those days, with banners on the pages that still describe `CDBSENDCREATE` as the runtime reader.

- Chapters 1–10 carried forward and corrected where a loose sheet had been left as the authority
- Chapters 11–18 add keepers (live addresses and decompile lines), the WDW spine, specimen pages (P1040 pin bounds, P430, P420, P1170, TBX inventory), the OpenScript byte encoding including the superseded keyword mismatch, system-book tiers, the TBCBT cipher, the module list, and a row for every loose sheet
- `maps/bas-ne-to-ghidra.md` and `maps/wdw-to-ghidra.md` added. They are not typeset in the PDF
- Printable volume: `record/ToolBook-record-20261016.pdf`

## v0.0.1 — 2026-10-15

First release of the TBdecompile reference package.

- Contents: operational notes (object create path, graphics painters, OpenScript, open questions, debugger notes)
- Appendices: export maps, decimal/hex tables, Win16 system ordinals (KERNEL/USER/GDI), confirmed function names, ASCII lookup, symbol map excerpts
- Standalone landscape ASCII lookup table

The create-path wording in that release is superseded by the 2026-10-16 record.
