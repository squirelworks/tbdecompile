**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# TB80BAS.DLL-4.html — analysis

> Trail, 2026-10-16. Superseded. Chapter 4. Header correction stands: ordinal 51 is author-only. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80BAS.DLL-4.html`

## Coverage

- 25 runs of >20 `??` lines.
- 8 runs contain `C8` (ENTER prologue).
- Known functions present: `CDBPAINTPOLYGON`, `CDBSCALETWIPSTOSCREEN`, `CDBSENDCREATE`, `FUN_12c8_0850`, `FUN_12c8_0ef8`.

## New functions

28 functions are in the HTML but not in the C decompile. Most are in segment 1008. These are string helpers and standard prologues, not the record reader.

## Record reader

- No literal `14 00 00` in the HTML.
- `CMP AX,0x14` hits are bounds checks, not a stream walker.
- `LODSW` hits are in the OPTLOADER segment, not the record reader.

## Assessment

The HTML has the same coverage as the C decompile on the known interesting functions. The undisassembled regions are small and do not contain the record reader. Not a breakthrough.
