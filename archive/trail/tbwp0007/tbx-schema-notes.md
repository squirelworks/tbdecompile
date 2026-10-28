# TBX schema notes (2026-10-14)

> Trail, 2026-10-16. Chapter 2. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: SumTotal.ToolBook.XML.*.xsd files from Denny (TBSME).
These define the XML exchange format used between TB95 and TB115.
Not fully published. Saved under /workspace/attachments/.

## Key confirmations

### Bounds is primary

`DrawObject` (base for Rectangle, Polygon, IrregularPolygon, Ellipse, Arc, Pie, etc.)
requires a `Bounds` attribute:
```
<xs:attribute name="Bounds" type="Bounds" use="required"/>
```
Pattern: `-?\d{1,5},-?\d{1,5},-?\d{1,5},-?\d{1,5}`
This matches the four-word bounds we extract from the binary.

### Vertices is optional

`VectorObject` (base for Line, AngledLine, Curve, Arc, Pie) adds:
```
<xs:attribute name="Vertices" type="xs:string" use="optional"/>
```
Polygons and irregular polygons can be bounds-only. The tip shape
is expanded at paint or export time. Confirms P1040 pins.

### Object hierarchy

```
Object
  └─ ToolBookObject (IdNumber, Name, SharedScript, Script)
       └─ GraphicObject (RgbFill, RgbStroke, Transparent, Visible, ...)
            ├─ DrawObject (Bounds required, LineStyle, Pattern)
            │    └─ VectorObject (Vertices optional)
            │         └─ LineObject (LineEndSize, LineEndStyle)
            └─ TextObject (Bounds, FontFace, FontSize, FontStyle)
                 └─ FieldClass (Text, BorderStyle, FieldType, ...)
```

### Page structure

`Page` has:
- `Page.Objects` — sequence of Image, Arc, Button, Curve, Ellipse,
  Field, Group, IrregularPloygon (typo in schema), Line, PaintObject,
  Picture, Pie, Polygon, Rectangle, RoundedRectangle, Stage, etc.
- `Page.UserProperties`
- `Page.Actions`
- Attributes: Name, IdNumber (required), Background (required), Script,
  SkipNavigation, SharedScript, DefaultAllowDrop

### Book structure

`Book` has:
- `Book.Pages` — PageLocator list (IdNumber, Source path)
- `Book.Backgrounds` — BackgroundLocator list
- `Book.Resources` — Bitmap, Cursor, Font, Icon, Menubar, SharedScript, Clip
- `Book.Viewers`
- `Book.UserProperties`
- `Book.Actions`
- Size default `8640,5760` (6" × 4" at 1440 twips/inch)

### Resources

Bitmap resources have `KeyColor` and `UseChromaKey` for transparency.
SharedScript is a resource, not inline.

### Typo

Schema uses `IrregularPloygon` (missing 'y'). Match this when parsing
official TBX exports.

## Relation to binary

| TBX | Binary (9e954d01.tbk) |
|-----|-----------------------|
| Bounds attribute | four-word record + fill color |
| Vertices attribute | kind=0400 point list at +0x22 |
| RgbFill | fill dword at +4 |
| IdNumber | object id in page record |
| Name | 32-byte field at marker+11 |
| Script | OpenScript handler in page blob |

The XML is the expanded form. The binary stores bounds for most
shapes and expands vertices only for true polygons. The schema
confirms the bounds-only path is valid and expected.

## Next uses

1. Validate the 9e954d01 TBX export against these schemas.
2. Map binary record subtypes to the object types listed in
   `Page.Objects`.
3. Use Bounds/Vertices distinction to decide when to expand tips
   vs. store point lists in a modern renderer.
