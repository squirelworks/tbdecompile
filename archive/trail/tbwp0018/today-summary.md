# Today — 2026-10-14

> Trail, 2026-10-16. Chapter 10. Day log of 2026-10-14. Later corrections win. If this sheet and `TBdecompile/record/` disagree, the record wins.

## RTM analysis

- Triaged TB80RTM.EXE (163k lines). No 14 00 00 reader. No named file open.
- Property bus: `CDBSAVEBOOK`, `CDBGETVALUEEX`, `CDBSENDVALUEEX`, `CDBSETVALUEEX`.
- Nameable wrappers: `BEGINPAINT`, `ENDPAINT`, `CREATEWINDOW`, `DESTROYWINDOW`, `SHOWWINDOW`, `ENABLEWINDOW`, `SETFOCUS`, `GETFOCUS`, `INVALIDATERECT`, `ENDDIALOG`.
- Deep analysis: `GETDLGITEM` top ID is 0x65 (101, 55 hits). `GETWINDOWLONG` top index is 10 (196 hits). `FUN_1068_0098` is `GLOBALALLOC` with OOM retry. `FUN_1068_0000` is the dialog helper.
- Paint path: `WM_PAINT` handler calls `CLIENTTOPAGE` then `Ordinal_26` (`CDBPAINTCLIENT`). Shape drawing is in BAS, not RTM.

## BAS segment triage

- Sampled segments 1018, 1278, 1478, 14b8, 1508, 10d0, 1030, 14a8, 1160, 1070. None contain a 14 00 00 reader.
- Side quests surfaced:
  - Graphics resource lifetime (1018/1098): pen/brush/bitmap creation and deletion
  - Object allocation (1478): near-object pool, 0x76-byte struct
  - Palette (1150/1030): `CREATEPALETTE`, `SELECTPALETTE`, `REALIZEPALETTE`
  - Field text rendering: `DRAWTEXT` reads from `param_5+0x4a/+0x4c/+0x50`
- Object struct: +0x3b is GDI handle, +0x1f is BitBlt raster op flag.

## Page / background index

- TBX P10213 references Background id 23. Binary page at 0x21db85 has no word/dword 23. Link is indirect.

## Property expansion

- `FUN_12c8_0ef8` copies `source+0x3e/+0x40/+0x42/+0x44` to `object+0x17/+0x19/+0x1b/+0x1d`. Disk 14 00 00 record does not match those offsets. Expansion step still unnamed.

## OpenScript

- Expression path: `FUN_1008_2d31` is the math dispatcher. Engine now handles `+ - * /` and `abs/sqrt/log/exp/sin/cos/atan/asin/acos`.
- Pushed openscript_analysis 1.0.0r5 and r6.

## Foolbook

- Content rectangle extraction added to `shapes.py`. Pattern is bounds at -16, fill at -4, marker `01 00 00 04`. 961 rectangles found in 9e954d01.tbk.
- Pushed as 0d4afc5.
- Research notes filed and published to Foolcourse, Foolversity, toolbookunpacker, TBWorldview.

## Decompile polish

- `SENDMESSAGE` and `LSTRLEN` arguments are mangled. Bookmarked for a re-decompile pass.

## Current goals

- Filed at `tbwp0018/current-goals.md`. Covers graphics, OpenScript, system books, object struct, page/background index, property expansion, decompile polish, and naming.
