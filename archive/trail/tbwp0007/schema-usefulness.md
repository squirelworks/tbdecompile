# Schema usefulness — investigation (2026-10-14)

> Trail, 2026-10-16. Chapter 2. Bounds required, Vertices optional, IrregularPloygon typo. If this sheet and `TBdecompile/record/` disagree, the record wins.

## What the schema confirmed

1. **Bounds is required** on every DrawObject. The binary four-word records
   are the canonical form. No surprise, but now documented.

2. **Vertices is optional** on VectorObject. Bounds-only is valid.
   The tip shape is not stored; it is computed.

3. **Object type list** matches the binary: Rectangle, IrregularPolygon,
   Arc, Curve, Field, Button, Picture, Stage, Group.

## What the TBX export revealed

P1040 (Page880) in the TBX export:

| Object | Count | Notes |
|--------|-------|-------|
| IrregularPolygon | 28 | Pins, all with Vertices |
| Rectangle | 2 | Bodies |
| Arc | 2 | |
| Field | 5 | |
| Button | 3 | |
| Group | 5 | |

First pin in TBX:
```
Vertices="5055,4605,5205,4605,5205,4733,5175,4767,5160,4825,5145,4860,5115,4860,5100,4825,5085,4767,5055,4733,5055,4698"
```

Binary record at page+0x3e4:
```
5055, 4605, 5205, 4860  then  00 00 00 00 c0 c0 c0
```

The binary stores the bounding box. The TBX export expands the tip.
The numbers match at the start. The tip is computed, not stored.

P430 (Page875) has 96 IrregularPolygons with Vertices. The binary had
22 kind=0400 polygons plus many bounds records. The export expands
everything.

## Breakthrough

The schema + TBX export together show the expansion direction:

```
binary bounds  →  TBX Vertices
```

The missing "reader-to-bounds" function is the inverse of what TB115
does on Save To XML. The binary is the compact form. The XML is the
expanded form.

This does not locate the function in the decompile, but it confirms
the data flow and the expected input/output.

## What it did not do

- Did not name the function that reads the 14 00 00 record.
- Did not give the exact layout of the bounds record beyond the
  four words + fill.
- Did not reveal how the tip is computed (the expansion algorithm).

## Practical use

The TBX export is now the reference for expected output. A binary
parser that produces the same Vertices lists as the TBX export is
correct. The schema defines the target format. The binary defines
the source. The gap is the expansion step.
