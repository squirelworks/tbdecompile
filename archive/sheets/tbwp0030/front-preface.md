# Preface

**Date:** 16 October 2026

Four sheets sit in front of the contents. Each one is its own file, so any one of them can be printed without the others.

| Sheet | File |
|---|---|
| Cover | `cover.pdf` |
| Table of contents | `toc.pdf` |
| Preface | `preface.pdf` |
| Foreword | `foreword.pdf` |

The table of contents is the sheet that changes first. It lists the files in the edition and, inside the contents, the chapter titles taken from the record. It does not contain the chapters. Reprint it on its own when a chapter or an appendix has been added and the contents file has not been typeset yet. Replacing that sheet does not require printing the record again.

The contents file is the files in `TBdecompile/record/`, copied whole, in order, beginning with the reading guide. A chapter was not shortened to fit a page, and it was not cut in the middle of a paragraph. The reading guide is part of the contents. It is not a second preface. The grades (Known, Thought, Conjecture, Not true, Superseded) are defined there.

If a later edition of the contents does not fit under 100 pages, the break goes between chapters.

Appendices are not in the contents file. Each one is its own document. None of them is a slice of the narrative, and the narrative is not a slice of them.

| File | What it holds |
|---|---|
| Appendix A | BAS, RTM, and W16 export maps, and the BAS ordinal map. Copied whole from the 12 October map notes. |
| Appendix B | Architecture and the gaps. Replaces the 15 October architecture appendix. |
| Appendix C | TBX, against the exported specimen. Replaces the 15 October TBX appendix. |
| Appendix D | NE-segment and one-boot WDW address maps. Each of those files, complete. |
| Appendix E | Decimal/hex 0–255, ASCII 0–127, and the Win16 KERNEL/USER/GDI ordinals from the 15 October lookups. |
| Appendix F | Confirmed function names, the 15 October table, carried forward whole. |
| Appendix G | SoftICE. Commands, the screen, and the book-open read from the night of 15 October. |
| Appendix H | The Watcom debugger. Commands, the screen, and what the three export traces did not find. |
| Appendix I | Assembly, read beside the Ghidra C, so a listing is not trusted just because it compiled into C. |
| Appendix J | OpenScript. The byte classes, the two decoder bugs, the handlers that expand, and what the player does not do. |
| Appendix K | How to disassemble. How Ghidra turns seeds into instructions, how a name differs from a purpose and an operation, and the passes this project uses to finish a listing. |

When this manual and `TBdecompile/record/` disagree, the record wins.
