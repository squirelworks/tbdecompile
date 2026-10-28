# TB80RTM.EXE-2.c — new decompile

> Trail, 2026-10-16. Chapter 17. SENDMESSAGE / LSTRLEN arguments want a fresh decompile. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80RTM.EXE-2.c` (32,656,279 bytes)

## Findings

- Property bus present: `CDBGETVALUEEX`, `CDBSENDVALUEEX`, `CDBSETVALUEEX`.
- Paint path present: `Ordinal_26` (`CDBPAINTCLIENT`) called from the paint handler.
- No `??` markers. The listing is fully decompiled.
- 261 `halt_baddata` hits. 19 `FUN_15a8_*` / `FUN_15b0_*` / `FUN_15b8_*` / `FUN_15c0_*` functions at the end are garbage (data misidentified as code). Same class of noise as the BAS decompile.

## Usefulness

- Same quality as the previous RTM triage. The property bus and paint path are confirmed.
- The garbage at the end is ignorable.
- Worth keeping as the working decompile if the old one is not available.

## Not a breakthrough

No 14 00 00 reader. No named file open. Shape drawing is still in BAS, not RTM.
