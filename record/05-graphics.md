# 5. Graphics

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| G-001 | Superseded | Polygon kind `04 00` with an inline point list at `+0x22`. | The specimen's class `0x10` keeps the count at `+0x30` and a near pointer at `+0x32`. G-002. `research/store-20261022.md`. |
| G-012 | Known | A resource id is the fourth word of the 8-byte directory entry. A button stores that id plus one, at graphics-block `+0x15`. | `FUN_1128_1e44` accepts a match only when the scanned word is the fourth. 396/396 buttons. |
| G-002 | Known | The polygon painter is BAS `FUN_1408_0376` (segment `0x82` offset `0x376`). It copies object `+0x30` / `+0x32` to `DS:30AC` and calls `GDI!POLYGON`. | SoftICE, 2026-10-10 |
| G-003 | Known | Content rectangles are bounds-only. In the page blob the tail is four twip words, a zero dword, a fill dword, then `01 00 00 04`. `9e954d01.tbk` has 961 of that marker. | Foolbook `shapes.py` count, P1040 |
| G-004 | Known | An arc object is type `0x11`. Four twip pairs at `+0x25`, `+0x29`, `+0x2D`, `+0x31`. Bounds at `+0x0F`. Fill at `+0x18`. Painter is BAS segment `0x7B`. | live arc, 2026-10-10 |
| G-005 | Known | ToolBook does not call `GDI!PIE`. Pie wedges are computed by `GDIELLIPSEPOINTFROMANGLE` (property `0x4123`) and filled with the arc geometry. | import table and decompile |
| G-006 | Known | A diagram bracket on P1170 is not stored as points. BAS segment `0x5B` computes four polyline points from the object bounds. | live `GDI!POLYLINE`, 4 points |
| G-007 | Thought | P420’s flame is several pen strokes in the record at page `+0xA13`, matching three 96-point red IrregularPolygons in the TBX export. The on-disk control structure is not known. | render attempts, TBX |
| G-008 | Known | A live button holds its four picture ids in the block at `+0x28`. Normal id at block `+0x15`, invert `+0x27`, disabled `+0x39`, checked `+0x4B`. | `research/paint-20261021.md` |
| G-009 | Known | A stored bitmap is an 8-byte prefix, then a Windows BMP. `9e954d01.tbk` has 67. Use `bfSize` from the `BM` header. The prefix dword is not always `bfSize + 8`. | same note, file scan 2026-10-21 |
| G-010 | Known | Resource directories are one per type. `FUN_1028_218a` reads `OBJGETHDRLONG((type + 5) * 4)`. Type 1 is a bitmap. `TB80BMP` is not the lookup. | same note. One Bochs hit returned an object reference for type 9 |
| G-011 | Known | Draw-object pattern `+0x25`, stroke `+0x17`, fill `+0x1B`. Background pattern `+0x4B`, fill `+0x5B`, size `+0x5F` / `+0x61`. `0xFD` is hollow, `0xFE` solid paper, `0xFF` solid ink. | same note |

## 5.1 Who paints

The painters live in `TB80BAS`. They are reached through a type dispatcher, not by a named call from outside BAS. `TB80RTM` handles `WM_PAINT` only as far as `CLIENTTOPAGE` and `CDBPAINTCLIENT` (ordinal 26).

| Painter | Where | GDI |
|---|---|---|
| `PaintPolygon` | `1408:0376` | `POLYGON` |
| `PaintPolyline` | `13e8:00E6` | `POLYLINE` |
| `PaintRectangle` | `1020:03E4`, and segment `0x83` (`FUN_1410_0066`) | `RECTANGLE` |
| `PaintArc` / alt | `10A0:0558`, `10A0:0458` | `ARC` |
| `PaintEllipse` | `1230:2F1C` and an alt | ellipse |
| `PaintRoundRect` | `1230:2278` and alts | round rect |
| `ScaleTwipsToScreen` | `1008:01DD` | none. Converts in place. |

`FUN_1008_01dd` is that converter. For each pair it computes `(coord * factor + 0x2D0) / 0x5A0`. `0x5A0` is 1440, one inch in twips. `0x2D0` is 720, so the add is rounding. The x factor is `DAT_1630_01a6` and the y factor is `DAT_1630_01a8`. At 96 DPI the factor is 96 and the division is the same as dividing by 15. The `/15` rule is that case, not the function.

The polygon type table is not in the static image. Unpacked BAS still carries Optloader segment-table debris. The HTML listing has zero cross-references to `FUN_1408_0376`. **Thought.** The table is built at load, or fixed up by an NE relocation that the listing does not show as a pointer. A break on the painter, then one frame up, is how the table gets found. Searching the file for the bytes `76 03 08 14` will not find it. The selector is assigned at load.

`SetPointArray` (`FUN_1408_00d8`, property `0x4050`) stores the count at `+0x30`, allocates `count * 4` with `OBJNEWNEAR` into `+0x32`, and copies the points. That is the runtime setter. The file does not contain a `0x4050` record.

`LOCKPATTERN` (`1098:0876`) takes a pattern index at `[BP+0xC]`, accepts 1 through `0x80`, and calls `TOOLBOOKFATAL` outside that range. `UNLOCKPATTERN` is `1098:09FC`. It is a fill hatch, not a picture id. An earlier listing also saw a pattern index at object `+0x17` and `+0x5B`. `+0x17` is already the four-word copy in chapter 4. Do not treat those two notes as the same field until both are dumped on one object.

The October 12 field card puts the polygon’s object pointer at `[BP+4]`. A far call’s first argument, after `ENTER`, is `[BP+6]` (the manual’s assembly card). The card did not record whether `PaintPolygon` was entered by a near call or a far call. Dump both slots once. The count at `+0x30` and the points at `+0x32` do not depend on that.

## 5.2 What is stored

**Polygons.** `9e954d01.tbk` has 96 kind-`0400` records on 13 pages. P430 has 22. A broader search that ignores the kind word produces false positives. P430 draws as a chip: silver pins (`0xC0C0C0`) and a light-gray body (`0xE0E0E0`). One live 11-point polygon is a pin tip, not the body. The captured screen points were `(218,335)` through `(218,341)`, a 10 by 17 notch. The same points exist in the file as twips near page offset `0x9CB` of P430: `(3147,3862)` through `(3147,3973)`.

Pins that share identical point bytes stack on top of each other until the index at `+0x52` is applied. That index is not applied in the current clean-room draw.

**Rectangles.** P1040 is the TTL intro page (TBX page id 880). Two DIP packages: 7400 on the right, 5400 on the left. The 8.1 file stores 28 pin boxes (fill `0xC0C0C0`) and two dark bodies (fill `0x404040` in the TBX, `64,64,64`). The pin tip is not an 11-point list on this page. Paint expands the tip. The TBX export writes the expanded Vertices. Matching a TBX Vertices list back to the binary means matching the bounding box, not searching for 11 points.

**Brackets and strokes.** On P1170 the bracket’s live polyline was `(354,201) (321,201) (321,238) (358,238)`. The object bounds in twips were left `4801`, top `3015`, right `5370`, bottom `3570`. Divided by 15 that is the same rectangle. The points are computed. Connecting lines and detail strokes of this kind are not extracted yet.

**Arcs.** Live geometry is known (G-004). Fill `0x808080` was seen at `+0x18`. No page record has been matched to type `0x11`, and the start and sweep angles are not located in the struct. Do not set a breakpoint on `GDI!PIE`. The call is not imported.

**Curves.** Curve’s type id in `nc81base.sbk` is `0x05C7` (file offset `0x1810`). That id is not in the P420 page records. The point runs sit in the record at page `+0xA13`. A naive walk draws a tangle in screen space around 400–500. The TBX export of the flame is three 96-point red IrregularPolygons. **Thought.** The tangle is strokes concatenated that should be drawn separately. A length prefix or a zero terminator between groups has not been proven. There is no `Curve` name on the page.

**Pictures.** A button's four picture ids are in the block at live record `+0x28` (G-008). The bytes are an 8-byte prefix and then a BMP (G-009). `9e954d01.tbk` has 67 of them. The lookup is the per-type directory in G-010, not `TB80BMP`. A picture that is not a button still has no located id. `DRAWPICTURECALLBACK` writing a GDI handle at object `+0x0C` / `+0x0E` remains a reading of the listing, not a live dump. An earlier note said 641 BMPs carved. That count is a header scan, not a widget binding, and it is not the number to use.

The shared near-start graphic in the lesson books is a 581 by 157, 8 bpp gold plate, not a text banner. Two notes locate the `nida81` splash building: file `0x413FAB` (323 by 344, 8 bpp, off-bits 310) and a carved copy taken from file `0x487BE` (27874 bytes). This record does not treat those two offsets as the same byte. The live `BITMAP` header that was found was width `0x143`, height `0x158`, 8 bpp, stride `0x258`, `bmBits` null. **Known** that the splash is a DIB. **Not known** which property on the page object holds its id.

BAS segment `1150` builds the book palette (`CREATEPALETTE`, `SELECTPALETTE`, `REALIZEPALETTE`). An 8 bpp BMP needs that palette. Segment `1018` creates and deletes pens, brushes, and bitmaps. Who owns the lifetime is open. Fill color and stroke color are known (G-011). Pen width is not.

Field text is `DRAWTEXT` from a paint context at `param_5+0x4A`, `+0x4C`, and `+0x50`. The disk handle is word 1 of the block at object `+0x24` (O-009). Word 0 of that block is the style-run handle. The rest of the field layout, including the border, is open.

## 5.4 Classes, from the 21 October listing

`FUN_1058_2ae4` registers the draw segment. This does not retire G-002. The note is `research/paint-20261021.md`.

| Class | Draw segment | Record | What it calls |
|---|---|---|---|
| 8 | `0x1410` | `0x28` | `FUN_1410_0066`, `RECTANGLE` |
| `0xC` | `0x13d8` | `0x28` | `FUN_13d8_0066`, `ELLIPSE` |
| `0xD` | `0x13e0` | `0x2C` | `FUN_13e0_015a`, `ROUNDRECT`. Corner radii at `+0x28` and `+0x2A` |

The ellipse previously listed in segment `1230` is not this registration. Bounds for all three are `+0x0F`, `+0x11`, `+0x13`, `+0x15`. Class `0xF` is registered with a `0x34`-byte record. It is not yet named polygon.

## 5.3 What a render is allowed to claim

A clean-room picture of a page is not the engine (WV-005). The current honest draw is:

1. Explicit point records (kind `0400`) where the count and the pairs are in the file.
2. TBX Vertices where an export exists and the binary only stored bounds.
3. A bounds rectangle where neither points nor an export exist.

Say which of the three was used. P430 from kind `0400` is a check against the chip. P1040 from bounds is a check against the two packages, with the understanding that the pin tips are fatter on screen than the stored boxes. P420 from a raw point dump is not a flame until the stroke breaks are known.
