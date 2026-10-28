# PaintPolygon type-table: what can be done from the files

> Trail, 2026-10-16. Chapter 5. Table is runtime-built. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What was tried

1. NE relocation dump against segment 0x82.
2. Static XREF search in TB80BAS.DLL.html for `FUN_1408_0376` / `1408:0376`.
3. Registrar check on `FUN_1058_0a98`.

## Results

### NE image is not clean

`/workspace/artifacts/Toolbook/_unpacked/TB80BAS.DLL` and `tbworkingpapers/tbwp0002/TB80BAS_noghidra.DLL` both have:

- `ne_cseg = 64`
- Segment table entries with nonsense lengths and flags (length 32784, flags 0001, sectors in the 30k range).

This is still the OPTLOADER/self-loading form. The earlier "199 segments" figure was `ne_maxalloc` / `ne_ovno` (0xc7 = 199), not the segment-table count. A relocation dump that targets "segment 0x82" cannot be done on this image; there is no segment 0x82 in a 64-entry table, and the table itself is not a normal NE segment table.

### No static XREF

`TB80BAS.DLL.html` contains exactly one hit for `1408:0376` / `FUN_1408_0376`: the function definition itself. Ghidra did not resolve any caller. The type table is not a static far call.

### Registrar is property setup, not the painter table

`FUN_1058_0a98` writes `0x4034` (the vertices property id) into `object+0x68` in several places. That is the property-setter registration, not a type-to-painter function-pointer table.

## What remains

The type table that reaches `PaintPolygon` is built at runtime (or fixed up by the NE loader after segments are mapped). From the files on disk it is not visible.

To see it:

- Under SoftICE or WDW, once a book is open and a page with polygons is painted, break on the type-dispatcher segment (previously seen as BAS 0x7E / selector 3617 that boot).
- Dump the table it indexes. The entry that leads to `PaintPolygon` will be a far pointer whose offset is `0x376` and whose selector is whatever BAS segment 0x82 was loaded as on that boot.
- Alternatively, break on `PaintPolygon` itself (BAS segment 0x82 offset 0x376, selector moves per boot) and walk the stack one frame up; the return address is inside the dispatcher, and the table index is on the stack or in a register.

Neither of those can be done from the static files.
