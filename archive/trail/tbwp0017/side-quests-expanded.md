# Side quests — expanded

> Trail, 2026-10-16. Chapter 10.5. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Graphics resource lifetime

`FUN_1098_0be0` creates a GDI object, stores the handle in `DAT_1630_309e`, and calls `FUN_1098_0cda`. On failure it `DELETEOBJECT`s the handle. This is a cache: the handle is kept in DGROUP and reused.

`FUN_1098_0d86` selects an object from `param_2 + 0x3b` and calls `BITBLT`. The raster op depends on a flag at `param_2 + 0x1f`:
- bit 2 clear: `SRCCOPY` (0xcc0020)
- bit 2 set: `NOTSRCCOPY` (0x8800c6)

`param_2 + 0x3b` is a handle in the object struct. `param_2 + 0x1f` is a flag byte.

`FUN_1018_0cbe` is another `BITBLT` caller. It reads flags at `DAT_1630_01e0 + 0x6f` and builds a raster-op mask.

Side quest: map the handle slots in the object struct. `+0x3b` is one. The pen and brush are likely nearby. A live break on `CREATEPEN` with the object pointer in a register would name them.

## Object allocation

`FUN_1478_014a` computes a rounded size (`(param_1 + param_3 - 1) / param_1 * param_1`) and calls `FUN_1478_00a0`. That is the near-object pool. The 0x76-byte object struct comes from here.

Side quest: who calls `FUN_1478_00a0` with 0x76? That is the object constructor. It is adjacent to the create path but not the record reader.

## Palette

`FUN_1150_0081` builds a palette and calls `HCACHEPURGE`. `FUN_1030_0000` is the first `SELECTPALETTE` caller. `REALIZEPALETTE` has 8 hits.

Side quest: the palette is built from the book, not from the BMP. The 8bpp BMPs we carved need the book's palette to display correctly. The load path is in 1150.

## Field text rendering

`CREATEFONT` is near `GETTEXTMETRICS` and `SELECTOBJECT`. `TEXTOUT`, `DRAWTEXT`, and `EXTTEXTOUT` are in the same region. `DRAWTEXT` reads from `param_5 + 0x50`, `+0x4a`, and `+0x4c`. Those are likely the font, color, and alignment fields of the text object.

Side quest: the field text we already extract is painted by this path. Mapping `+0x4a`/`+0x4c`/`+0x50` gives the font and color without a live trace.

## None of these are the record reader

They are the paint and load paths that a reimplementation has to get right once the reader is found.
