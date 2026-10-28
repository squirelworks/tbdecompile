# BAS segment triage — next pass

> Trail, 2026-10-16. Chapter 4. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Already walked

- 1008: FPU/math dispatcher (`FUN_1008_2d31`), string/memory helpers. Not the record reader.
- 1280: second-highest density. Sampled; no stream walker.
- 1170: third-highest. Sampled; no stream walker.
- 1028: filter registrar (`FUN_1028_2680`). Closed.
- 12c8: create path. Sparse. No reader.

## This pass

| Segment | Functions | Character | 14 00 00 reader? |
|---------|-----------|-----------|------------------|
| 1018 | 45 | GDI helpers (`DELETEOBJECT`, `SETRECT`). Resource cleanup. | No |
| 1278 | 130 | Memory/pointer checks. `FUN_1278_00fa` is `ISBADREADPTR(0x14)`. | No |
| 1478 | 32 | Object allocation (`OBJNEWNEAREX`, array sizing). | No |
| 14b8 | 33 | Table lookup / property helpers. | No |
| 1508 | 45 | Structure walking, some string. No byte-compare stream. | No |

None of the five contain a function that walks a far pointer and compares the first word to `0x0014`.

## Next

The remaining high-density segments that have not been sampled are `10d0` (275), `1030` (273), `14a8` (249), `1160` (234), and `1070` (207).

`10d0` is the nearest unexamined segment to the create path (12c8). It is the next place to open.

The reader is still more likely to be in RTM than in any of these BAS segments. A live break on `CDBFILEOPEN` remains the higher-yield path.
