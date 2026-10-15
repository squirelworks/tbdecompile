# 8. Naming

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| N-001 | Known | Eight modules were counted for pattern coverage: 10,991 unique functions, 1,918 nameable by pattern, 17.5 percent. | `toolbook_naming_progress.md`, 2026-10-11 |
| N-002 | Known | Confirmed renames, after the later digs, are 112: BAS 20, then BMP, RTM, CMP, UTL, W16, LNL, MM, RCR, FLT, NET, JPG, and VBX. | `naming_summary.md` through 101, then JPG +1 and VBX +6 |
| N-003 | Known | A pattern name is not a confirmed name. The nameable lists are candidates. The rename scripts are the ones that were applied. | `TBdecompile/rename/` |
| N-004 | Known | Coverage by module, pattern only: RTM 32.7 percent, UTL 41.1, BMP 26, BAS 17.4, W16 17.3, LNL 12.2, CMP 5.6. | progress table |

## 8.1 What the numbers mean

“Nameable” means the decompiler text matches a pattern: a GDI call, `GLOBALALLOC`, `SENDMESSAGE`, a string move. “Confirmed” means a person or a script renamed that one function because the body matches the name. The gap between 1,918 and 112 is mostly unreviewed candidates, not unknown programs.

The 30 percent target in the October 11 note was a counting goal, not a research goal. Naming another thousand `StrCpy` wrappers will not find the record reader.

## 8.2 Confirmed painters and neighbors

These are the names later chapters use. Addresses are Ghidra `segment:offset` on the image those scripts were run against. Selectors move. Offsets inside the NE segment do not, once the segment is identified.

| Name | Address | Module |
|---|---|---|
| `PaintPolygon` | `1408:0376` | BAS |
| `PaintPolyline` | `13e8:00E6` | BAS |
| `PaintRectangle` | `1020:03E4` | BAS |
| `PaintArc` | `10A0:0558` | BAS |
| `PaintEllipse` | `1230:2F1C` | BAS |
| `PaintRoundRect` | `1230:2278` | BAS |
| `ScaleTwipsToScreen` | `1008:01DD` | BAS |
| `SetProperty` | `12D0:03EC` | BAS |
| `SetPointArray` | `1408:00D8` | BAS |
| `SetupPaintRect` | `12D0:086C` | BAS |
| `SetScriptProperty` | `1008:03F6` | BAS |
| `Lz77Expand` | `1000:0031` | BMP |
| `CreateDibBitmap`, `BitBltBmp`, `SelectPaletteBmp` | BMP rename script | BMP |
| `LoadCompilerResource`, `ExpandTextCore` | CMP rename script | CMP |
| `PaintPageRect` | `1398:05C6` | RTM |

Ellipse, round-rect, and a second arc painter were added in the same BAS pass. They are real GDI wrappers. They are not evidence that every shape in a lesson is stored as that GDI call’s arguments. Chapter 5 is the rule for storage.

## 8.3 Scripts

Java and Python rename scripts live in `TBdecompile/rename/`. Copies of the nameable TSV files live under `TBWorldview/Modules/tb80*_knownnames/`. The scripts rename only when the old `FUN_` name is still present. They do not invent names for functions that do not match the body.

Ghidra `CodeN` is not the NE segment number. Use `TBdecompile/maps/` before typing a segment into a debugger.

## 8.4 What is still thin

`TB80RCR` exports are only partly named. The `TB80UTL` classification strings are known. They are not yet tied to the kind bytes inside `14 00 00` chunks. CMP is 5.6 percent pattern-nameable because most of it is the compiler, not a wrapper around a Windows API. A name on a CMP function is useful when it is `COMPILEREXPANDTEXT`. A name on a CMP function that only moves a token is not.
