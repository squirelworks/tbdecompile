# TB80RTM.EXE-4.html — undisassembled regions

> Trail, 2026-10-16. Chapter 17. ?? runs. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80RTM.EXE-4.html`

## Coverage

- 113 runs of >20 `??` lines.
- 73 runs contain `C8` (ENTER prologue).
- Largest runs: 1571, 1103, 1067, 964, 876 lines.

## Comparison with C decompile

- C decompile has 726 `FUN_1110_*` hits.
- HTML has undisassembled regions that the C decompile has decompiled.
- The HTML is a raw disassembly; the C decompile has more analysis.

## Assessment

The HTML has large undisassembled regions with ENTER prologues. These are real functions that Ghidra did not flow into. The C decompile has already covered these regions. The HTML is useful as a cross-reference but not a breakthrough.

## Worth forcing disassembly

The 73 ENTER runs could be force-disassembled if the C decompile is incomplete. The C decompile already covers the known interesting functions.
