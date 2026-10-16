# Graphics painters (TB80BAS)

> Duplicate of `TBdecompile/20261012/`. Do not edit this copy. The current statement is `record/`.

Confirmed from the decompile and SoftICE traces.

## Painters

| Function | Segment:offset | Role | Notes |
|----------|----------------|------|-------|
| `FUN_1408_0376` | 1408:0376 | PaintPolygon | Count at object+0x30. Calls `SetupPaintRect`, `ScaleTwipsToScreen` on DS:30AC, then `GDI!POLYGON`. |
| `FUN_1410_0066` | 1410:0066 | PaintRectangle | Reads bounds at object+0xF, calls `GDI!RECTANGLE`. |
| `FUN_1008_01dd` | 1008:01dd | ScaleTwipsToScreen | `screen = (stored * DPI + 720) / 1440`. At DPI 96: stored/15. |
| `FUN_10a0_0558` / `FUN_10a0_0458` | 10a0 | Arc helpers | Live object type 0x11, four twip pairs, fill at +0x18. |
| `FUN_1408_00d8` | 1408:00d8 | SetPointArray | Runtime property 0x4050 setter. Not on disk. |

## On-disk polygon (solved)

- Signature: `14 00 00` subtype-0, `+0x0c = 04 00`.
- Fill dword at +4.
- Point count at +0x1A.
- x,y twip pairs start at +0x22.
- Screen = twips/15.
- 96 such records on 13 pages in 9e954d01; P430 has 22.

## Still open

| Item | Status |
|------|--------|
| Curve control structure (P420) | Points exist at page+0xA13. No count/header recovered. Render is a tangle. |
| Arc disk layout | Live object known. No matching `14 00 00` pattern tied on disk. |
| Picture id → DIB | 641 BMPs carved. Widget field that holds the id not identified. TB80BMP ordinal 3 is the reader. |
| Computed shapes (brackets) | Segment 0x5B builds them from bounds. Not stored points. |

## Scale function (recovered)

```c
// FUN_1008_01dd — simplified
// For each x,y pair:
//   screen_x = (stored_x * DAT_1630_01a6 + 0x2d0) / 0x5a0
//   screen_y = (stored_y * DAT_1630_01a8 + 0x2d0) / 0x5a0
// DAT_1630_01a6 / 01a8 = 96 on the observed boot → /15.
```
