**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# TB80BAS.DLL-4.c — new decompile

> Trail, 2026-10-16. Superseded. Chapter 4. Same correction. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80BAS.DLL-4.c` (58,849,798 bytes)

## Findings

- Core functions present: `CDBSENDCREATE`, `FUN_12c8_0850`, `FUN_12c8_0ef8`.
- Previously undisassembled regions are now decompiled. `FUN_12e8_0000` (OLE clone) is present and looks real.
- 8 `swi(3)` hits and 13 `FUN_16a8_*` functions at the end are garbage (data misidentified as code). These are the same class of noise as the old decompile.
- No `??` markers. The listing is fully decompiled.

## Usefulness

- Better coverage of the previously undisassembled regions.
- Same quality on the core functions.
- The garbage at the end is ignorable.
- Worth keeping as the working decompile if the old one is not available.

## Not a breakthrough

The 14 00 00 reader is still not visible. The create path is the same. Property expansion offsets still do not match the disk record.
