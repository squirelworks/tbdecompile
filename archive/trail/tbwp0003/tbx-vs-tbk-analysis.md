# 9e954d01 TBX vs TBK Comparison

> Trail, 2026-10-16. Chapters 2 and 13. Bounds in 8.1, Vertices in the export. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Source:** SumTotal ToolBook TBKX export of the Logic Families lesson (`9e954d01 tbx/` folder).
**Compared against:** Prior reverse-engineering of the raw `9e954d01.tbk` (JBO at file offset 0xC00, 129 pages reported earlier).

Date: 2026-10-13

## Structure Overview

| Item | TBX | TBK (prior notes) | Notes |
|------|-----|-------------------|-------|
| Pages | 131 | 129 | TBX includes all named pages P0–PINFO. Small delta likely from counting method or two system/info pages. |
| Backgrounds | 14 | (not previously counted as separate) | Explicit Background*.xml + .script |
| Bitmaps | ~72–77 external .bmp | Embedded Windows BMPs | TBX extracts them as BitmapNNN.bmp |
| Scripts | 302 external .script files | Compressed OpenScript bytecode in page records | TBX is plain source text |
| Object types (top) | IrregularPolygon 654, Line 528, Field 497, Button 382, Group 371, Rectangle 243 | Earlier extractor found only 96 kind=0400 polygons on 13 pages | Major difference — see below |

Book caption: "Nida Corporation - Logic Families"
Page size: 9360×6624 twips (standard ToolBook; screen ≈ /15).
MinorVersionNumber: 664

## Geometry Storage — Key Difference

**TBK (binary):**
- Pins and many shapes stored as **bounding boxes** inside `14 00 00` records (fill color at +4, e.g. 0xC0C0C0).
- Full point lists only in specific records (e.g. P430 pin tips had count at +0x1a and pairs at +0x22; P420 curve points buried in a large blob).
- Arc/ellipse geometry often computed or stored as type-specific fields, not expanded vertices.
- Earlier polygon renderer matched only a subset of records.

**TBX (XML):**
- Every IrregularPolygon has an explicit `Vertices="x1,y1,x2,y2,..."` attribute in twips.
- Rectangles have `Bounds="left,top,right,bottom"`.
- Arcs have short `Vertices` (often 2 points) plus other attributes.
- Groups nest the objects that form a visual unit (chip package, flame, etc.).

### Example: P1040 (TTL intro, two DIP packages)

Already broken down in tbwp0007. Confirmed here:

- 28 IrregularPolygons (11-point pin tips, fill 192,192,192).
- 2 Rectangles (chip bodies, fill 64,64,64).
- Nested Groups for left (5400) and right (7400) packages.
- In the raw TBK the same pins appear as bounds-only records; the XML expands the tip shape.

### Example: P430 (chip diagram)

- 96 IrregularPolygons on this page alone (many identical 11-point pin tips, offset in x).
- 8 Groups, 8 Rectangles, 8 Arcs.
- Matches the earlier live GDI!POLYGON traces (11-point notches) but the binary only exposed a fraction of them as explicit point records.

### Example: P420 (flame)

- IrregularPolygons with very long Vertices lists (one dark-red, one brighter red).
- These are the flame curves that previously rendered as a tangle when the point order was taken from the raw record.
- Also 18 AngledLines.

## Scripts

- Book.script contains the known enterSystem handler that pushes `tb80r.sbk`, `nc81base.sbk`, `nc81test.sbk`, `nc81recs.sbk`, `nc81trnr.sbk` and calls the initialize* / openSession functions.
- Per-object .script files are plain OpenScript (`to handle buttonClick`, `go to page "Pxxxx"`, `send next`, etc.).
- In the TBK these are the compressed bytecode streams previously decoded with the resource 0x77 keyword table.

## Resources

- Bitmaps are external files (Bitmap100.bmp …).
- No embedded OLE or other complex resources in the export examined so far.
- Backgrounds are first-class objects with their own XML.

## Implications for the Runtime / Viewer

1. The TBX is a much more convenient source for accurate geometry than the raw TBK.
2. A clean-room renderer can now use the Vertices/Bounds attributes directly instead of reverse-engineering every `14 00 00` layout.
3. The large number of IrregularPolygons (654 total) explains why earlier binary walks under-counted shapes.
4. Scripts can be used as-is for a playback engine; no further bytecode decoding needed for this lesson.

## Next Steps (suggested)

- Extract all Vertices lists into a simple JSON or SVG set for visual verification.
- Diff page names and object counts against any future raw TBK dump.
- Use the TBX as the reference for the Foolbook / viewer geometry layer.


## Direct TBK Comparison (2026-10-13)

Raw file: `/workspace/attachments/9e954d01.tbk` (2,327,983 bytes).
JBO signature at file 0xC00: `03 4A 42 4F 01 00 00 08`.

| Metric | TBK | TBX | Notes |
|--------|-----|-----|-------|
| Page objects (80 65 markers) | 129 | 131 Page.xml | TBX extras: **P440** and **P2920** |
| All other named pages | 129 | 129 | Perfect match (P0, P1, P10, P100, P300, P400, P420, P430, P900, P1001, P1040, …) |
| P1040 page | offset 0x19BE3A, 7764 bytes | Page880/Page.xml | Matches prior notes. 29 × 0xC0C0C0 dwords in the page. |
| Pin storage | Bounds-only records | Explicit 11-point Vertices | Confirmed |
| P420 flame | Point data inside large record | 3 × 96-point red IrregularPolygons | TBX has the ordered vertices |

The binary page count of 129 matches the earlier reverse-engineering notes. The TBX export adds two pages that do not appear as 80 65 page records in the TBK.

