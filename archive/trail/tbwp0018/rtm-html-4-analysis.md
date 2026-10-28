# TB80RTM.EXE-4.html — analysis

> Trail, 2026-10-16. Chapter 17. RTM is the paint handoff. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80RTM.EXE-4.html`

## Coverage

- 113 runs of >20 `??` lines.
- 73 runs contain `C8` (ENTER prologue).
- 31 functions are in the HTML but not in the C decompile.

## New functions

Most are in segment 1008. These are standard prologues and math helpers, not the record reader.

## Record reader

- No literal `14 00 00` in the HTML.
- `CMP AX,0x14` hits are bounds checks, not a stream walker.

## Assessment

The HTML has the same coverage as the C decompile on the known interesting functions. The undisassembled regions are large but the new functions are helpers. Not a breakthrough.
