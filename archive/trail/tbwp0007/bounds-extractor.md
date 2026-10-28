**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Bounds extractor and content rectangles (2026-10-14)

> Trail, 2026-10-16. Superseded. Chapters 5 and 13. The 14 00 00 01 becomes 11 hypothesis in the header era is not true (WV-010). If this file and `TBdecompile/record/` disagree, the record wins.

## Status

The record-to-bounds step is still not located in the decompile. The create path is known. The on-disk patterns are known. A practical extractor can be written from the patterns.

## Known create path

```
CDBSENDCREATE (12c8:00bc, Ordinal_51)
  └─ FUN_12c8_0850
       └─ FUN_12c8_0e32
            └─ FUN_12c8_0ef8   ← writes bounds to object+0xf..+0x15
```

`FUN_13d0_0822` in RTM calls `Ordinal_51`. Type codes 0x401–0x40e map to object types (0x401 → 0x27, 0x404 → 0x0e, 0x405 → 0x11 arc, etc.).

## On-disk patterns (from P1040 and P430)

### Bounds-only rectangles (content bodies, pin placement)

Pattern in the page blob:
```
left top  right bottom  00 00 00 00  c0 c0 c0 00  01 00 00 04
```
- Four words: left, top, right, bottom (twips).
- Fill color dword follows (0xC0C0C0 silver, 0x404040 dark gray for bodies).
- Screen = twips / 15.
- P1040: 28 pin records + 2 body rectangles. Tips are expanded at paint time, not stored.

### Polygon records (vertex lists)

`14 00 00` subtype-0 with `+0x0c = 04 00`:
- Fill dword at +4.
- Point count at +0x1A.
- x,y twip pairs at +0x22.
- Runtime: SetPointArray (0x4050) copies to object+0x30/+0x32. PaintPolygon scales and calls GDI!POLYGON.
- Per-pin offset is the index at +0x52 (not yet applied in renderer).

## Practical extractor

A bounds extractor can walk the page blob for the four-word pattern and the kind=0400 polygon records. The missing piece is the live caller that reads the record and passes the four words into `CDBSENDCREATE`. That caller is not a named export in the current BAS decompile.

## Remaining research

1. XREF `CDBSENDCREATE` from the RTM page-open path. `FUN_13d0_0822` is one caller. Trace its callers.
2. Search BAS for the signature bytes `14 00 00` near a bounds read. The reader may be in a load-on-call segment not yet named.
3. SoftICE: break on `FUN_12c8_0ef8` and walk the stack when a known rectangle is created. Capture the source pointer and the record header.

## Content rectangles

Closed for practical purposes. The bounds-only pattern is consistent across P1040 pins and bodies. The tip shape is computed at paint time from the bounds. No vertex list is stored for those records.
