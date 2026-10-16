# Graphics painters (TB80BAS)

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

Confirmed from the decompile and SoftICE traces.

| Function | Address | Role |
|----------|---------|------|
| `FUN_1408_0376` | 1408:0376 | PaintPolygon. Reads count at object+0x30, points at object+0x32. Calls GDI!POLYGON. |
| `FUN_1008_01dd` | 1008:01dd | ScaleTwipsToScreen. `(stored * DS:01A6 + 720) / 1440`. At DPI 96 this is /15. |
| `FUN_1408_00d8` | 1408:00d8 | SetPointArray. Runtime property 0x4050 setter. Not on disk. |
| `FUN_12d0_03ec` | 12d0:03ec | SetProperty. Routes 0x4034. |
| Segment 0x83 | 1410:0066 | Simple rectangle painter. Reads bounds at object+0x0F, calls GDI!RECTANGLE. |
| Segment 0x7B | 1408:058A | Arc painter. Type 0x11. Four twip pairs at +0x25. Fill at +0x18. |

## On-disk polygon

- Signature: `14 00 00` subtype-0, `+0x0c = 04 00`.
- Fill dword at +4.
- Point count at +0x1A.
- x,y twip pairs start at +0x22.
- Screen = twips/15.
- 96 such records on 13 pages in 9e954d01; P430 has 22.

## Still open

- Curve control structure (P420). Points exist at page+0xA13. No count/header recovered.
- Arc disk layout. Live object known. No matching `14 00 00` pattern tied on disk.
- Picture id → DIB. 641 BMPs carved. Widget field that holds the id not identified.
- Computed shapes (brackets). Segment 0x5B builds them from bounds.
