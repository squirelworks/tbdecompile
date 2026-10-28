# Approach correction — 2026-10-14

> Trail, 2026-10-16. Kept. Chapter 4. Do not close a function for lacking the literal. If this file and `TBdecompile/record/` disagree, the record wins.

## The mistake

Closing candidates with "not the 14 00 00 reader" on the basis of the HTML listings. The HTML is not a complete disassembly. It has large `??` regions and data sections that Ghidra did not turn into code. A function that reads a 14 00 00 record can still sit in an undisassembled area.

## What the HTML actually covers

- ~4847 FUNCTION markers
- ~31k data-section lines
- 99 code segments with widely varying line counts
- Leading bytes of some segments are still `??`

"Not found in the HTML" means "not in the disassembled portion," not "not in the binary."

## Correction

Do not treat absence from the HTML as proof of absence. When a candidate is closed, note that the closure is only for the disassembled portion. Undisassembled regions remain open until they are either disassembled or shown by a runtime trace to be unrelated.

## Cost

Static searches that only confirm "not in the listing" are low-value. Prefer:

- Runtime traces that show which code actually runs on a page open or paint.
- Targeted disassembly of regions that the HTML left as data or `??`, when there is a reason to suspect them.
- Keeping notes on what was not covered, so later work does not re-search the same gap.
