# TB80RTM.EXE-4.html — HTML listing

> Trail, 2026-10-16. Chapter 17. Listing note. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80RTM.EXE-4.html` (53,990,928 bytes)

## Findings

- Property bus present: `CDBGETVALUEEX`, `CDBSENDVALUEEX`, `CDBSETVALUEEX`.
- Paint path present: `Ordinal_26` (`CDBPAINTCLIENT`) called from the paint handler.
- 91,290 `??` markers. Large undisassembled regions.
- 242 `halt_baddata` hits in the C decompile. The HTML has more noise.

## Usefulness

- Same quality as the previous RTM triage on the known functions.
- The HTML has more undisassembled regions than the C decompile.
- Worth keeping as a cross-reference if the C decompile is not available.

## Not a breakthrough

No 14 00 00 reader. No named file open. Shape drawing is still in BAS, not RTM.
