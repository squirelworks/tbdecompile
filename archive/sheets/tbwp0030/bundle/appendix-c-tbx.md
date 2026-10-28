# Appendix C — TBX File Format

Schema, and what the exported specimen actually contains.

**Date:** 16 October 2026

**Status:** This appendix replaces the 15 October 2026 TBX appendix. The schema and the specimen are the same ones. Counts that the record has since settled are stated at the grade the record gives them. This file does not absorb the contents volume, and it does not absorb the export-map appendix.

## 1. What TBX is

TBX is the XML exchange format used by ToolBook 9.5 and 11.5. It is not the on-disk TBK format. It is the expanded, human-readable form produced by File → Save To XML when `saveSpecial=true` is set in `Instructor115.ini`.

A TBKX package is a ZIP of a TBX folder. The folder contains `Book.xml`, one `Page.xml` per page, `Background.xml` files, `.script` files, and resource files (bitmaps and the rest).

Namespace: `urn:sumtotalsystems:toolbook.tbkx`.

The 11.5 specimen exists. An earlier note that called the export a conjecture is closed. Saving from the 11.5 trial converts the book. An 8.1 runtime cannot open that converted file.

## 2. Schema hierarchy

Taken from the published schema, not from a guess at the binary.

```
Object
  +-- ToolBookObject (IdNumber, Name, SharedScript, Script)
        +-- GraphicObject (RgbFill, RgbStroke, Transparent, Visible)
              +-- DrawObject (Bounds required, LineStyle, Pattern)
              |     +-- VectorObject (Vertices optional)
              |           +-- LineObject (LineEndSize, LineEndStyle)
              +-- TextObject (Bounds, FontFace, FontSize, FontStyle)
                    +-- FieldClass (Text, BorderStyle, FieldType)
```

Bounds is required on every DrawObject. The pattern is left, top, right, bottom in twips, each an integer of at most five digits, optional leading minus.

Vertices is optional on VectorObject. Bounds-only is valid. The tip shape is expanded at paint or at export time. The binary stores the bounds. The XML writes the point list.

The schema spells IrregularPolygon wrong (`IrregularPloygon`). Official exports use that spelling. This appendix uses the schema's spelling when it is naming the element, and the ordinary spelling when it is naming the shape.

## 3. Book structure

```
Book
  +-- Book.Pages            PageLocator list (IdNumber, Source path)
  +-- Book.Backgrounds      BackgroundLocator list
  +-- Book.Resources        Bitmap, Cursor, Font, Icon, Menubar,
  |                         SharedScript, Clip
  +-- Book.Viewers
  +-- Book.UserProperties
  +-- Book.Actions
```

Size default on the schema is `8640,5760` (6 by 4 inches at 1440 twips per inch).

From the `9e954d01` export the book element is:

```
Book Script="Book.script" Caption="Nida Corporation - Logic Families"
     Size="9360,6624" MinorVersionNumber="664"
     xmlns="urn:sumtotalsystems:toolbook.tbkx"
```

## 4. Page structure

```
Page
  +-- Page.Objects          Image, Arc, Button, Curve, Ellipse, Field,
  |                         Group, IrregularPloygon, Line, PaintObject,
  |                         Picture, Pie, Polygon, Rectangle,
  |                         RoundedRectangle, Stage, and the rest
  +-- Page.UserProperties
  +-- Page.Actions
```

Attributes include Name, IdNumber (required), Background (required), Script, SkipNavigation, SharedScript, and DefaultAllowDrop.

The `9e954d01` export contains 131 `Page.xml` files. The 8.1 binary has 129 `80 65` page records. All 129 names match a TBX page. Two XML pages, P440 and P2920, have no page record in the binary. They are an export addition, not a page the binary walk missed.

## 5. Object examples from 9e954d01

P1040 (TBX page id 880) is the TTL intro. Two DIP packages.

| Element | Count | Note |
|---|---|---|
| IrregularPloygon | 28 | Pins, all with Vertices |
| Rectangle | 2 | Bodies, fill `64,64,64` |
| Arc | 2 | |
| Field | 5 | |
| Button | 3 | |
| Group | 5 | Left package at 5400, right package at 7400 |

The first pin's Vertices begin `5055,4605,5205,4605` and continue through the tip, ending at the same outline. The binary record at that location stores the bounding box `5055, 4605, 5205, 4860`, then a zero dword and the fill. The numbers match at the start. The tip is computed, not stored. TBX expands it.

## 6. P430 and P420

P430 is the chip diagram. The TBX page carries 96 IrregularPloygon elements with Vertices, plus 8 Groups, 8 Rectangles, and 8 Arcs. The live `GDI!POLYGON` traces of this page include an 11-point notch. The binary does not store 96 kind-`0400` point records on this page. It stores 22. The rest of the TBX polygons are expansions of bounds-only records. Counting XML elements and counting kind-`0400` records answer different questions. Both counts stand.

P420 is the flame. The TBX page has IrregularPloygon elements with very long Vertices lists, one dark red and one brighter red, matching three 96-point strokes, plus 18 AngledLines. Taking point order from the raw record rendered a tangle. The on-disk control structure for those strokes is still unknown. The TBX list is the expanded form, not a dump of the chunk.

## 7. Scripts

`Book.script` contains the `enterSystem` handler that pushes `tb80r.sbk`, `nc81base.sbk`, `nc81test.sbk`, `nc81recs.sbk`, and `nc81trnr.sbk`, and calls the `initialize*` / `openSession` functions.

Per-object `.script` files are plain OpenScript:

```
to handle buttonClick
  go to page "P400"
end
```

In the TBK those handlers are compressed bytecode. In TBX they are already expanded. The export of this specimen has 302 `.script` files, counting the book script and the per-object scripts.

## 8. Resources

Bitmaps are external files (`Bitmap100.bmp` and the rest). The specimen has about 75 BMPs. Bitmap resources carry `KeyColor` and `UseChromaKey` for transparency. 8.1 stores an imported picture as a basic blob and turns it into a BMP. 11.5 stores WMF, JPG, TIF, BMP, PNG, and GIF as themselves.

SharedScript is a resource, not inline. No embedded OLE or other complex resources were found in this export.

Backgrounds are first-class objects with their own XML and `.script` files. The specimen has 14 backgrounds. A TBX page can name a background by an id that does not appear as a word or a dword in the matching binary page. The link is indirect. The field that holds it has not been located.

## 9. TBX against TBK

| TBX attribute | Binary, in `9e954d01.tbk` |
|---|---|
| `Bounds="l,t,r,b"` | Four twip words, plus a fill |
| `Vertices="x,y,..."` | Kind `0400` point list at `+0x22`, or a bounds-only record whose tip the export expanded |
| `RgbFill="r,g,b"` | Fill dword |
| `Script="..."` | Bytecode in the page blob |
| `IdNumber` | Page or object id |
| `Background` | Not a direct word in the decoded page record. The link is indirect. |

TBX is the expanded form. A clean-room renderer can use Vertices and Bounds directly instead of reconstructing every `14 00 00` layout, and it should say which one it used.

## 10. Counts from the 9e954d01 specimen

| Item | Count |
|---|---|
| `Page.xml` | 131 |
| `80 65` page records in the 8.1 file | 129 |
| XML pages with no binary page | 2 (P440, P2920) |
| Backgrounds | 14 |
| `.script` files | 302 |
| Bitmaps | about 75 |
| IrregularPloygon elements | 654, across all pages |
| Kind-`0400` point records | 96, on 13 pages |

The large XML polygon count is why a binary walk that only counts explicit point records under-counts shapes. Many pins are bounds-only in the TBK and become point lists only in the TBX.

## 11. What a reader can take from this

TBX is a convenient source for the expanded geometry. Vertices and Bounds can be used directly. Scripts can be used as source. No bytecode decode is required for this lesson if the TBX is the input.

A reader that must also handle a raw TBK:

- Use the TBX as the reference for what the expanded form should look like.
- Treat a bounds-only binary record as complete for the box and incomplete for the tip. The tip is computed.
- Groups in the TBX show which objects form a visual unit. A run of ascending words inside a binary page is an offset directory, not a Group.
- P440 and P2920 have no binary counterpart. Do not go looking for an `80 65` record that is not there.
