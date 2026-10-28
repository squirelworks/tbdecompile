**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# TB80BAS.DLL-4.html — HTML listing

> Trail, 2026-10-16. Superseded. Chapter 4. Same correction. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80BAS.DLL-4.html` (75,722,204 bytes)

## Coverage

- 25 runs of >20 `??` lines.
- 8 runs contain `C8` (ENTER prologue).
- Largest runs: 1473, 365, 295, 277, 113 lines.

## Comparison with C decompile

- C decompile has 6397 `FUN_10b0_*` and `FUN_12e8_*` hits.
- HTML has fewer undisassembled regions than the RTM HTML.
- Known functions present: `PaintPolygon`, `ScaleTwipsToScreen`, `CDBSENDCREATE`.

## Assessment

The HTML has fewer undisassembled regions than the RTM HTML. The C decompile already covers the known interesting functions. The HTML is useful as a cross-reference but not a breakthrough.

## Worth forcing disassembly

The 8 ENTER runs could be force-disassembled if the C decompile is incomplete. The C decompile already covers the paint path and object creation.
