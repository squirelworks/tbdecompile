# P1040 raw TBK breakdown (9e954d01.tbk)

> Trail, 2026-10-16. Chapter 13.1. Bounds, fills, blob offsets. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: /workspace/attachments/9e954d01.tbk
Page name: P1040
File offset: 1687098 (0x19C03A)
Page blob length: 7764 bytes
Quoted jumps: P1050 (Next), P1001 (Back)

## Key finding

The raw TBK does **not** store the 11-point pin vertex lists that appear in the TBKX XML export.
Each pin is stored as a **bounding box** (left, top, right, bottom) followed by the fill color.
The tip shape is expanded at export or paint time.

## Pin records (28 total)

Pattern in blob (example at 0x3e4):
```
left top  right bottom  00 00 00 00  c0 c0 c0 00  01 00 00 04  ...
```
Fill is 0xC0C0C0 (192,192,192). Screen = twips / 15.

### Group 53 — 7400 (right)

Bottom pins (y base 4605):
| Offset | Bounds (twips) | Screen ≈ |
|--------|----------------|----------|
| 0x03e4 | 5055,4605–5205,4860 | 337,307–347,324 |
| 0x044c | 5460,4605–5610,4860 | 364,307–374,324 |
| 0x04b4 | 5880,4605–6030,4860 | 392,307–402,324 |
| 0x051c | 6315,4605–6465,4860 | 421,307–431,324 |
| 0x0584 | 6705,4605–6855,4860 | 447,307–457,324 |
| 0x05ec | 7125,4605–7275,4860 | 475,307–485,324 |
| 0x0654 | 7560,4605–7710,4860 | 504,307–514,324 |

Top pins (y base 3300):
| Offset | Bounds (twips) | Screen ≈ |
|--------|----------------|----------|
| 0x071c | 5055,3300–5205,3555 | 337,220–347,237 |
| 0x0784 | 5460,3300–5610,3555 | 364,220–374,237 |
| 0x07ec | 5880,3300–6030,3555 | 392,220–402,237 |
| 0x0854 | 6315,3300–6465,3555 | 421,220–431,237 |
| 0x08bc | 6705,3300–6855,3555 | 447,220–457,237 |
| 0x0924 | 7110,3300–7260,3555 | 474,220–484,237 |
| 0x098c | 7530,3300–7680,3555 | 502,220–512,237 |

### Group 52 — 5400 (left)

Bottom pins (y base 4605):
| Offset | Bounds (twips) | Screen ≈ |
|--------|----------------|----------|
| 0x0b6c | 1680,4605–1830,4860 | 112,307–122,324 |
| 0x0bd4 | 2085,4605–2235,4860 | 139,307–149,324 |
| 0x0c3c | 2505,4605–2655,4860 | 167,307–177,324 |
| 0x0ca4 | 2940,4605–3090,4860 | 196,307–206,324 |
| 0x0d0c | 3330,4605–3480,4860 | 222,307–232,324 |
| 0x0d74 | 3750,4605–3900,4860 | 250,307–260,324 |
| 0x0ddc | 4185,4605–4335,4860 | 279,307–289,324 |

Top pins (y base 3300):
| Offset | Bounds (twips) | Screen ≈ |
|--------|----------------|----------|
| 0x0ea4 | 1680,3300–1830,3555 | 112,220–122,237 |
| 0x0f0c | 2085,3300–2235,3555 | 139,220–149,237 |
| 0x0f74 | 2505,3300–2655,3555 | 167,220–177,237 |
| 0x0fdc | 2940,3300–3090,3555 | 196,220–206,237 |
| 0x1044 | 3330,3300–3480,3555 | 222,220–232,237 |
| 0x10ac | 3735,3300–3885,3555 | 249,220–259,237 |
| 0x1114 | 4155,3300–4305,3555 | 277,220–287,237 |

## Chip bodies (Rectangles)

| Package | Offset | Bounds (twips) | Screen ≈ | Fill |
|---------|--------|----------------|----------|------|
| 7400 | 0x09f4 | 4875,3555–7830,4605 | 325,237–522,307 | 64,64,64 |
| 5400 | 0x117c | 1500,3555–4455,4605 | 100,237–297,307 | 64,64,64 |

## Fields

| Name | Bounds offset | Text offset | Notes |
|------|---------------|-------------|-------|
| Text | 0x9c | 0x1553 | TTL intro paragraph |
| Next | 0xe4 | — | Jump "P1050" |
| Back | 0x202 | — | Jump "P1001" |
| 7400 | 0x3c9 | 0x16af | Label |
| 5400 | 0xb51 | 0x16db | Label |
| DISCUSSION | 0x1261 | 0x1ba5 | Title |

## Notes

- Arcs from the XML (2-point vertices) were not found as raw point pairs; they may be stored as a different record type or computed.
- The earlier polygon extractor that looked for `+0x0c == 04 00` and a point count at `+0x1a` does not match these pin records. The pins here are bounds-based.
- This page is P1040. P420 was a different page (flame/curve) in the earlier notes.
