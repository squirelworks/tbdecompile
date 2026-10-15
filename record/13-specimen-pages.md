# 13. Specimen pages

Every number in this chapter is from `9e954d01.tbk` (Logic Families) or from its ToolBook 11.5 Save To XML, unless a path says otherwise. Screen pixels are stored twips / 15 at 96 dpi.

The binary has 129 pages, each a record starting `80 65 00 05 00 02 02`. The export has 131 `Page.xml` files. P440 and P2920 have no `80 65` record. They are an export addition. All 129 binary names match a TBX page.

TBX folder names (`Page880`) are export ids, not the runtime page name (`P1040`). IdNumber 880 is page `P1040`.

## 13.1 P1040 — two DIP packages, bounds only

File offset `0x19C03A` (1687098). Page blob 7764 bytes. Background id 2. Next goes to `P1050`. Back goes to `P1001`.

The 8.1 file does not store the 11-point pin tips that the XML writes. Each pin is four twip words, a zero dword, fill `0xC0C0C0`, then marker `01 00 00 04`. The tip is expanded at paint, and the export writes that expansion as Vertices. The book has 961 copies of the `01 00 00 04` marker. P1040 uses 28 of them for pins and 2 for bodies.

### 7400, right package

Body at blob `0x09F4`: bounds `4875, 3555, 7830, 4605`, screen about `325,237–522,307`, fill `64,64,64` (`0x404040`). Label field text `7400`.

Bottom pins, top `4605`, bottom `4860`:

| Blob offset | Bounds (twips) | Screen about |
|---|---|---|
| `0x03E4` | `5055–5205` | `337,307–347,324` |
| `0x044C` | `5460–5610` | `364,307–374,324` |
| `0x04B4` | `5880–6030` | `392,307–402,324` |
| `0x051C` | `6315–6465` | `421,307–431,324` |
| `0x0584` | `6705–6855` | `447,307–457,324` |
| `0x05EC` | `7125–7275` | `475,307–485,324` |
| `0x0654` | `7560–7710` | `504,307–514,324` |

Top pins, top `3300`, bottom `3555`:

| Blob offset | Bounds (twips) | Screen about |
|---|---|---|
| `0x071C` | `5055–5205` | `337,220–347,237` |
| `0x0784` | `5460–5610` | `364,220–374,237` |
| `0x07EC` | `5880–6030` | `392,220–402,237` |
| `0x0854` | `6315–6465` | `421,220–431,237` |
| `0x08BC` | `6705–6855` | `447,220–457,237` |
| `0x0924` | `7110–7260` | `474,220–484,237` |
| `0x098C` | `7530–7680` | `502,220–512,237` |

The first pin's bounds `5055, 4605, 5205, 4860` are the start of the TBX Vertices list. That is the expansion direction: bounds in the 8.1 file, point list in the XML.

### 5400, left package

Body at blob `0x117C`: bounds `1500, 3555, 4455, 4605`, screen about `100,237–297,307`, same fill `64,64,64`. Label `5400`.

Bottom pins, y `4605–4860`: `0x0B6C` `1680–1830`, `0x0BD4` `2085–2235`, `0x0C3C` `2505–2655`, `0x0CA4` `2940–3090`, `0x0D0C` `3330–3480`, `0x0D74` `3750–3900`, `0x0DDC` `4185–4335`.

Top pins, y `3300–3555`: `0x0EA4` `1680–1830`, `0x0F0C` `2085–2235`, `0x0F74` `2505–2655`, `0x0FDC` `2940–3090`, `0x1044` `3330–3480`, `0x10AC` `3735–3885`, `0x1114` `4155–4305`.

TBX group ids: 53 is the 7400 package, 52 is the 5400 package, 58 is the discussion title (gold plate button, graphic "bitmap id 149", plus a white "DISCUSSION" field and a blue drop shadow). The widget still does not name that bitmap inside the 8.1 object. See chapter 5.

Intro field bounds `600, 600, 8805, 2490`. Next button `8907, 6210, 9342, 6630`. Back button `-3, 6210, 432, 6630`.

## 13.2 P430 — kind `04 00` polygons, including a live pin tip

`9e954d01.tbk` has 96 kind-`0400` records on 13 pages. P430 has 22. A search that ignores the kind word produces false positives.

Record layout: fill dword at `+4`, kind `04 00` at `+0x0C`, count word at `+0x1A`, twip pairs at `+0x22`. The painter is `FUN_1408_0376`. It copies object `+0x30` / `+0x32` to `DS:30AC` and calls `GDI!POLYGON`.

P430 draws as a chip: silver pins (`0xC0C0C0`) and a light-gray body (`0xE0E0E0`). One live 11-point polygon is a pin tip, not the body. Captured screen points ran `(218,335)` through `(218,341)`, a 10 by 17 notch. The same points are in the file as twips near page offset `0x9CB`: `(3147,3862)` through `(3147,3973)`.

Pins that share identical point bytes stack until the index at object `+0x52` is applied. The clean-room draw does not apply it.

## 13.3 P420 — the curve that is not yet a flame

Points sit at page `+0xA13`. Curve's type id in `nc81base.sbk` is `0x05C7` (file offset `0x1810`). That id is not in the P420 page records. A naive walk draws a tangle in screen space around 400–500. The TBX export is three 96-point red IrregularPolygons. There is no `Curve` name on the page.

**Thought.** The tangle is strokes concatenated that should be drawn separately. A length prefix or a zero terminator between groups has not been proven. Do not treat a raw dump of `+0xA13` as the flame.

## 13.4 P1170 — the bracket is computed, and the word table is an index

Live polyline: `(354,201) (321,201) (321,238) (358,238)`. Object bounds in twips: left `4801`, top `3015`, right `5370`, bottom `3570`. Divided by 15 that is the same rectangle. BAS segment `0x5B` computes the four points. They are not stored.

The 27 ascending words at page `+0x8C3` are an offset directory into a `14 00 00 83` blob, not a Group. On this page the blob is file `0x1AB651`, 1844 bytes, and the word table is file `0x1ABE97`. The words begin `0x14, 0x16, 0x40, 0x52, 0x66, 0x7A, 0xC2` and are relative to the blob. Script-like markers inside the blob (`buttonClick`, `"P1180"`, `"P1140"`) sit at blob `+0xA9`, `+0xB9`, `+0x17B`, `+0x18B`. After those regions are set aside, the table still points at short structured runs (type bytes, small integers, `0xFFFFFF`). A Group is its own object and has its own member list.

## 13.5 P400 record sizes

P400 is 7046 bytes and 12 records. The early walk, kept because the sizes show what a "page of widgets" actually is:

| # | Page offset | Length | Kind | Note |
|---|---|---|---|---|
| 0 | `+0x2B` | 33 | `0001` | Small. |
| 1 | `+0x4C` | 31 | `0000` | Small. |
| 2 | `+0x6B` | 18 | `0D00` | Small. |
| 3 | `+0x7D` | 1458 | `D900` | Content blob: scripts and colors. |
| 4 | `+0x62F` | 2828 | `0021` | Large. Not a polygon. |
| 5 | `+0x113B` | 894 | `0000` | Count word at `+0x1A` is 21, not a kind-`0400` polygon. |
| 6 | `+0x14B9` | 156 | `1600` | Small. |

## 13.6 Lesson jumps that have been read

| Page | Handler |
|---|---|
| P900 | TTL → P1001. Other → P2001. Final quiz → P10001. Exit → `nida81` P20001. No Next. |
| P1001, P2001 | Back returns to P900, not to `nida81` P20001. |
| P300 | `selection1` sends `lastbook nida81.tbk` and `nextpage` P310. |
| P10001 | Directions → `nida81` P10020. Exit → `nida81` P20001. Begin → P10210. |
| P10410 | Menu returns to P900. |
| P1290 | Correct choice 5408. Again → P1292. Next → P1300. |
| P20000 of `nida81.tbk` | `buttonClick` goes to P20001 because the handler says so. |

## 13.7 TBX draw inventory

Tag counts across the `9e954d01` export. These are XML tags, not kind-`0400` records. A page can have hundreds of IrregularPolygons that the 8.1 file stored as bounds.

| Kind | Count |
|---|---|
| IrregularPolygon | 654 |
| Line | 528 |
| Field | 497 |
| Button | 382 |
| Group | 371 |
| Rectangle | 243 |
| AngledLine | 66 |
| Arc | 62 |
| Ellipse | 45 |
| Hotword | 5 |

Pages whose export folder contains at least one IrregularPolygon. Columns are IrregularPolygon, Rectangle, Line, AngledLine, Arc, Ellipse, Group, Field.

| TBX folder | Poly | Rect | Line | Angled | Arc | Ell | Group | Field |
|---|---|---|---|---|---|---|---|---|
| Page872 | 14 | 2 | 2 | 0 | 1 | 1 | 4 | 7 |
| Page873 | 44 | 5 | 0 | 0 | 2 | 2 | 2 | 4 |
| Page874 | 8 | 2 | 2 | 18 | 0 | 0 | 2 | 2 |
| Page875 | 96 | 8 | 2 | 1 | 8 | 0 | 8 | 1 |
| Page876 | 12 | 32 | 108 | 0 | 0 | 0 | 48 | 5 |
| Page880 | 28 | 2 | 0 | 0 | 2 | 0 | 5 | 5 |
| Page885 | 28 | 4 | 0 | 0 | 2 | 0 | 4 | 5 |
| Page887 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 8 |
| Page891 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 8 |
| Page897 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 8 |
| Page900 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 8 |
| Page901 | 42 | 3 | 0 | 0 | 3 | 0 | 3 | 4 |
| Page909 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 8 |
| Page912 | 42 | 3 | 0 | 0 | 3 | 0 | 5 | 7 |
| Page914 | 28 | 4 | 0 | 0 | 2 | 0 | 5 | 6 |
| Page915 | 42 | 3 | 0 | 0 | 3 | 0 | 5 | 7 |
| Page917 | 42 | 3 | 0 | 0 | 3 | 0 | 4 | 8 |
| Page918 | 42 | 3 | 0 | 0 | 3 | 0 | 4 | 8 |
| Page919 | 14 | 1 | 0 | 0 | 1 | 0 | 1 | 4 |
| Page923 | 28 | 2 | 0 | 0 | 2 | 0 | 5 | 5 |
| Page931 | 3 | 8 | 27 | 0 | 0 | 0 | 13 | 4 |
| Page932 | 9 | 28 | 81 | 0 | 0 | 1 | 37 | 5 |
| Page934 | 14 | 1 | 0 | 0 | 1 | 0 | 2 | 2 |
| Page940 | 6 | 22 | 54 | 0 | 0 | 2 | 24 | 5 |
| Page941 | 14 | 1 | 2 | 0 | 1 | 0 | 2 | 4 |
| Page943 | 14 | 1 | 2 | 0 | 1 | 0 | 2 | 4 |
| Page949 | 2 | 0 | 7 | 0 | 0 | 0 | 0 | 2 |
| Page961 | 12 | 32 | 108 | 0 | 0 | 0 | 49 | 7 |

Page880 is the P1040 export: 28 polygons, 2 rectangles, 2 arcs. The 28 polygons are the paint-time expansion of the 28 bounds records in section 13.1. Page875 (96 polygons, 8 arcs) is the dense drawing page in the export. It is not, by itself, proof of 96 kind-`0400` records.

## 13.8 Pictures, stated with the two offsets kept apart

Windows BMPs can be carved. One match against the export paired 67 markers with 72 TBX bitmaps. The widget does not name the bitmap. Compressed pictures go through `TB80BMP` ordinal 3 and have been followed as far as a far call at `0x1FCD`. `Lz77Expand` is BMP `FUN_1000_0031`.

The shared near-start graphic is a 581 by 157, 8 bpp gold plate, not a text banner.

Two notes locate the `nida81` splash and they are not the same byte: file `0x413FAB` (323 by 344, 8 bpp, off-bits 310), and a carved copy taken from file `0x487BE` (27874 bytes). The live `BITMAP` header that was found was width `0x143`, height `0x158`, 8 bpp, stride `0x258`, `bmBits` null. The splash is a DIB. Which property on the page object holds its id is not known.

Lesson picture counts from the early carve: 71 BM and 5 JPEG in the lesson, 76 BM and 12 JPEG in `nida81`. BAS segment `1150` builds the book palette. An 8 bpp BMP needs that palette. Which palette a given carved BMP must use is open.
