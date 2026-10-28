# Search for a Data-Segment Far Pointer to PaintPolygon (1408:0376)

> Trail, 2026-10-16. Chapter 5. No static far pointer to 1408:0376. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What was searched

- TB80BAS.DLL.html for the string `1408:0376`, `FUN_1408_0376`, and data-segment references.
- Unpacked binary `/workspace/artifacts/Toolbook/_unpacked/TB80BAS.DLL` for the little-endian far-pointer bytes `76 03 08 14` (offset 0x0376, segment 0x1408).

## Result

**Zero hits** for the byte pattern `76 03 08 14`.

The Ghidra label `1408` is a load-time selector (or a Ghidra-assigned segment number), not a constant stored in the file. A raw search of the on-disk image cannot find a far pointer that uses the live selector.

## What this means

The type table that reaches `PaintPolygon` (FUN_1408_0376) is one of:

1. **Built at runtime** — a registrar (FUN_1058_0a98 was previously noted as a per-type registrar) fills a table of function pointers after the segments are loaded.
2. **Stored as NE segment-index + offset** and fixed up by the loader. The on-disk form would be a relocation record, not the literal bytes `76 03 08 14`.
3. **A table of near offsets** into a common code segment, with the segment implied by the caller.

Prior notes already recorded that `PaintPolygon` has no external named XREF in the HTML and is reached via a type table (SoftICE: BAS segment 0x7E / selector 3617 that boot).

## Next cut

- Dump the NE relocation records that target segment 0x82 (PaintPolygon’s segment) and see which data locations are fixed up to 0x82:0376.
- Or break on the type-dispatcher segment (0x7E) under SoftICE/WDW and dump the table it indexes once the book is open.
- The registrar FUN_1058_0a98 (noted in the create-path writeup) is a candidate for the code that fills the table.
