# Research notes

> Trail, 2026-10-16. Chapter 9. If this sheet and `TBdecompile/record/` disagree, the record wins.

## Object struct (0x76 bytes)

From TB80BAS decompile and live traces:

- Bounds at `+0x0f` / `+0x11` / `+0x13` / `+0x15` (left, top, right, bottom, twips).
- GDI handle at `+0x3b`. `FUN_1098_0d86` selects this and calls `BITBLT`.
- Flag byte at `+0x1f`. Bit 2 selects the `BITBLT` raster op: clear is `SRCCOPY`, set is `NOTSRCCOPY`.
- Point count at `+0x30`, point array pointer at `+0x32` (4 bytes per point, stored twips).

`FUN_1478_00a0` is the near-object pool that hands out these structs. `FUN_1478_014a` is the array allocator that sizes by `param_1 * param_2` and calls it.

## Palette

8bpp BMPs in the books are not self-contained. They need the palette that `CREATEPALETTE` builds and `SELECTPALETTE`/`REALIZEPALETTE` installs. The load path is in BAS segment 1150 (`FUN_1150_0081`). Without it, a renderer shows the right pixels in the wrong colors.

## Field text

`CREATEFONT` is near `GETTEXTMETRICS` and `SELECTOBJECT`. `DRAWTEXT` reads from `param_5 + 0x50`, `+0x4a`, and `+0x4c`. Those are likely the font, color, and alignment of the text object.

## Graphics resource lifetime

`FUN_1098_0be0` creates a GDI object, stores the handle in `DAT_1630_309e`, and reuses it. On failure it `DELETEOBJECT`s. This is a DGROUP cache, not a per-object slot.

## Not the record reader

None of these are the 14 00 00 record reader. They are the paint and load paths that a reimplementation has to get right once the reader is found.
