# Object ids, as far as they are known

A polygon does not have one id. Three numbering systems are in use, and a value from one of them is not a value from the others. Do not merge them. Do not invent the missing names.

## 1. Live type word

The type sits at offset `-2` of the `0x76`-byte object. Only one value has a name taken from a live object.

| Type | Name | What is known |
|---|---|---|
| `0x11` | Arc | Seen live. Bounds at `+0x0F`. Four twip pairs at `+0x25`, `+0x29`, `+0x2D`, `+0x31`. Fill at `+0x18`. Painter is BAS segment `0x7B`. |
| `0x12` | Not named | `FUN_12c8_0ef8` leaves it alone, in the same arm as the arc. |
| `0x0F`, `0x10`, `0x13`, `0x14` | Polygon-like | That function allocates a point array with `OBJNEWNEAR(count << 2)`. It does not say which value is Polygon, IrregularPolygon, Line, or Curve. |
| `0x24` | Not named | Copies four words from the source and does something else the listing did not name. |
| anything else | Bounds object | The default arm copies the four bounds words only. |

`FUN_1028_2680` treats a type id below `0x14` as an index into a 20-entry code table. That is a slot count. It is not a name for type `0x14`.

## 2. On-disk record kind

This is the marker inside a page. It is not the live type byte.

| Marker | What it is |
|---|---|
| `04 00` at `+0x0C` | Polygon point record. Fill dword at `+4`, count at `+0x1A`, twip pairs at `+0x22`. `9e954d01.tbk` has 96 of these on 13 pages. P430 has 22. |
| `01 00 00 04` | Bounds-only rectangle tail. The 11.5 export turns many of these into Vertices. |
| `80 65 00 05 00 02 02` | Page record, not a shape. |
| `14 00 00` | Start of a widget chunk inside a page. The type byte inside that chunk is not mapped. |

The live polygon the painter uses is a different layout from the disk record. `PaintPolygon` (`1408:0376`) reads the count at `+0x30` and the point pointer at `+0x32`, converts twips, and calls `GDI!POLYGON`.

Screen pixels at 96 dpi are stored twips / 15, which is `(stored * 96 + 720) / 1440`.

## 3. Names with no live type number

The system-book name table, in the order recovered from the books, is:

ComboBox, Stage, Picture, Hotword, RecordField, PaintObject, Curve, AngledLine, Pie, Arc, IrregularPolygon, Polygon, Line, RoundedRectangle, Ellipse, Group, Field, Button, Rectangle, Page, Background, Book.

The only numeric id taken from that table is Curve, `0x05C7`, at file offset `0x1810` in `nc81base.sbk`. That value does not appear in the P420 page records. Do not treat `0x05C7` as the live type byte at object `-2`.

Painters that are known by entry point, and not by type id:

| Painter | Entry |
|---|---|
| Polygon | `1408:0376` |
| Polyline | `13E8:00E6` |
| Rectangle | `1020:03E4` and `FUN_1410_0066` |
| Ellipse | `1230:2F1C` |
| Round rectangle | `1230:2278` |
| Arc | BAS segment `0x7B` |
| Curve | Not known. The points exist. The stroke walker does not. |

## 4. Not this list

A subtype table that runs line `1`, rectangle `2`, round rectangle `3`, ellipse `4`, polygon `5`, pie `6`, arc `7`, curve `8`, under a master class of `0x12`, is not a result from this binary. No compare against those bytes has been shown. `0x12` in the live type word is an unnamed arm next to the arc. It has not been shown to be a draw-object class with eight subtypes.

Property ids (`0x4004` bounds, `0x4015` idNumber, `0x4023` script, `0x4034` vertices, and the rest of that `0x40xx` range) are property slots. They are not object types.

Create-path selectors (`0x1014`, `0x1015`, `0x1021`, `0x1022`, `0x3018` through `0x301B`, `0x3022`) choose which helper builds an object. They are not the type stored at `-2`.
