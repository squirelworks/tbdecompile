# Debugger notes (SoftICE / WDW)

> Duplicate of `TBdecompile/trail/20261012/`. Do not edit this copy. The current statement is `record/`.

From field notes and the corrected breakpoint discussion.

## SoftICE standing orders

- `BC *` before the next breakpoint. A live `GDI!POLYGON` breakpoint freezes SoftICE if the page scrolls.
- Selectors change every boot. Copy offsets. Remap selectors.
- `MAP TB80BAS` (or RTM, BMP, …) to get the live selector for a segment.
- Segment numbers in MAP output are hex.
- Do not search all of memory. Wide 80 65 searches can GPF the VM.
- A dump that is the SoftICE window or the DOS device chain (CON/AUX/PRN) missed.

## Correct breakpoint form

```
BC *
MAP TB80BAS
; read the selector for the segment you want (e.g. 0x82)
BPX <selector>:0376 DO "D SS:BP-4 L 4; D DS:30AC L 40"
G
```

**Invalid:** `BPX BAS(82):0376`  
SoftICE does not accept that notation.

## Useful offsets (stable)

| Function | Segment:offset | Notes |
|----------|----------------|-------|
| PaintPolygon | 1408:0376 | Object at [BP+04], count at +0x30, points at +0x32 |
| PaintRectangle | 1410:0066 | Bounds at object+0xF |
| ScaleTwipsToScreen | 1008:01dd | |
| CDBSENDCREATE | 12c8:00bc | Ordinal_51 |
| FUN_12c8_0850 | 12c8:0850 | Allocator caller |
| FUN_12c8_0ef8 | 12c8:0ef8 | Bounds writer |

## WDW

- Use the `.map` files as a lookup. Note the live selector, then set `selector:offset`.
- Or break on BAS ordinal 51 and read the return address to land in the caller.

## Dump cautions

- Real dumps: page.bin01511 (ASYM_TpID), p400.bin0157 (JBO signature), dump-001/002 (Viewer/System).
- Junk: console logs, DOS device chain, name-slot only.
- ICEDUMP 6.021 needs kernel32 and user32 exports in winice.dat. Memory-dump recipe is not repeatable.
