# Side quests from the segment samples

> Trail, 2026-10-16. Chapter 10.5. Real, and not the reader. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

The 14 00 00 reader is still missing. These are the interesting things that turned up while sampling the high-density segments.

## Graphics resource lifetime (1018, 1098)

`FUN_1018_0000` is a cleanup that calls `DELETEOBJECT` on two GDI objects stored in DGROUP. Segment 1098 has thin wrappers:

- `FUN_1098_0daa` — `CREATEPEN`
- `FUN_1098_0ec0` — `SELECTOBJECT` + `POLYGON` (already on the paint path)

`FUN_1018_0cbe` is a `BITBLT` caller. It checks flags at `DAT_1630_01e0 + 0x6f` and selects different raster ops.

Side quest: map the pen/brush/bitmap lifetime. Who creates them, where they live in the object struct, and who deletes them. This is the missing half of the paint path.

## Object allocation (1478)

`FUN_1478_00a0` calls `OBJNEWNEAREX`. `FUN_1478_014a` is an array allocator that sizes by `param_1 * param_2` and calls `FUN_1478_00a0`.

Side quest: the near-object pool. How objects get their 0x76-byte struct, and whether the pool is per-book or global. This is adjacent to the create path in 12c8 but not the record reader.

## Palette (1150, 1030)

`FUN_1150_0081` calls `CREATEPALETTE`. `FUN_1030_0000` is the first `SELECTPALETTE` caller. `REALIZEPALETTE` has 8 hits.

Side quest: the palette path. ToolBook books carry palettes; the 8bpp BMPs we carved need one. This is the load side of the picture path.

## Text (CREATEFONT, TEXTOUT, DRAWTEXT, EXTTEXTOUT)

`CREATEFONT` has 4 hits. `TEXTOUT` has 10, `DRAWTEXT` has 3, `EXTTEXTOUT` has 5.

Side quest: field text rendering. The engine already extracts field text. This is the GDI side of painting it.

## None of these are the record reader

The reader is still more likely in RTM. These are the side quests that the samples surfaced.
