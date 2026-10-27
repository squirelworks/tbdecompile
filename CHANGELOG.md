# Changelog

## v0.0.11r1 — 2026-10-27

- Chapter 9. Foollege and Foolcollege are the same layer. Foollege holds the students. It is not a second program, and it is not a running server. The v0.0.11 PDF still has the old sentence.

## v0.0.11 — 2026-10-27

- The printable book is one file, `manual/20261027/TBdecompile-v0.0.11.pdf` (172 pages), and the same book in parts. Cover, table of contents, preface, and foreword are separate. The contents are one file (58 pages). Each appendix is its own file. A part that would reach 100 pages is broken between headings. None of the parts did. `python3 manual/build.py` typesets them from `record/` and `manual/sources/`.

## v0.0.10r5 — 2026-10-25

- Chapter 15.7. The ToolBook 11.5 files named `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` are a 29,147-byte stub. They are not the Instructor 8.1 books in the size table.

## v0.0.10r4 — 2026-10-24

- The Reader session is `research/reader-20261024.md`. P400 is the INTRODUCTION page and the 74LS174N chip. Alt+Right is Next. F3 toggles Author. The erase rectangles are still unrecorded. Foolbook 1.0.5r32 still reads a polygon as an inline list and still hides the field named `correct`.

## v0.0.10r3 — 2026-10-22

- The specimen's object store is `research/store-20261022.md`. The page list is book `+0x10`. All 131 backgrounds resolve. A field is class `0xA`. A polygon outline is the block at `+0x32`. A bitmap id is the fourth directory word. Neither lesson book stores a password block.

## v0.0.10r2 — 2026-10-21

- Chapter 5. A button's picture ids are in the block at live `+0x28` (G-008). A stored bitmap is an 8-byte prefix and then a BMP; `9e954d01.tbk` has 67 (G-009). The lookup is a per-type directory in segment `1028`, not `TB80BMP` and not `TB80FLT` (G-010). Fill and stroke are G-011.
- Chapter 5.4. Class 8 is the rectangle, class `0xC` the ellipse, class `0xD` the rounded rectangle.
- Chapter 4.5. A live page names its background at `+0x47` / `+0x49`. The on-disk page is still not matched.
- Chapter 4.7. Script mode and script word by class, including the book at `+0x24`. A group's 10-byte child entry.
- Word 0 of a field's `+0x24` block is the style-run handle. The note is `research/paint-20261021.md`.

## v0.0.10r1 — 2026-10-21

- The author password is no longer printed. Chapter 16.6 keeps the stored bytes only.

## v0.0.10 — 2026-10-21

- A field's text handle is word 1 of the block at object `+0x24`. `FUN_1440_0160` does not read `+0x42`. Chapter 5's `DRAWTEXT` offsets stay the paint path.
- Segment 1278 loads class providers, not `sysBooks`. `a613` names `TB80ANM.SBK` and `TB80R.SBK`.
- Class `0x3A` is the book's `ClassTbl`. Class `0x26` is `Viewer`. The next free class number in the sample books is `0x3D`.
- The TBKX exports of `tb80r`, `tb80anm`, and `tb80hyp` contain the handler source. A scan for the words `to handle` does not.

## v0.0.9 — 2026-10-20

- Appendix L is the Bochs card. Chapter 7.6 points at it. The selectors from that boot are `maps/bochs-20261020.md`.
- Chapter 4.6. A lesson open reads an object body through `1178:08B2` → `1188:04DA` → `1188:08D6` → `1160:02CC`. `HUGEGETDATA` was not on that path. The handler for the traced handle is still open.
- Chapter 16.6. Empty-key `ENCRYPTEX` uses `BMWBMWBMW` at `DS:0x28`. The NIDA system books store `62 70 49 6a 7a`. That is the author password. The word is not printed. The keyed 10-byte path is still open. `cipher/empty_key.py` is the empty-key pair.
- Chapter 14. The plain-prefix counts are restated: 75 `buttonClick` and one `EnterPage` in `9e954d01.tbk`, and 100 `buttonClick` in `nida81.tbk`. The expander that matches this chapter is `openscript_analysis` `v1.0.0r9`.

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
