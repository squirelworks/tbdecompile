# Findings

> Trail, 2026-10-16. Object offsets from 14 October. Chapter 4 is the statement. A later live trace wins over this table. If this file and `TBdecompile/record/` disagree, the record wins.

The object is 0x76 bytes. These offsets are the ones the papers and the live traces agree on.

| Offset | What |
|---|---|
| `+0x0F` | Bounds, four words. Written from parameters, not read off the disk record |
| `+0x17` `+0x19` `+0x1B` `+0x1D` | Four words copied by `FUN_12c8_0ef8` from source `+0x3E` `+0x40` `+0x42` `+0x44` |
| `+0x1F` | BitBlt raster-op flag |
| `+0x30` | Point count |
| `+0x32` | Point array |
| `+0x3B` | A GDI handle |
| `+0x52` | A per-pin index. Not applied. Pins that share point bytes draw on top of each other |
| `-2` | A type byte. `0x11` is an arc. The other types are not mapped |

`CDBSENDCREATE` is `TB80BAS` ordinal 51, at `12c8:00bc`. It receives the bounds. It does not parse `14 00 00`. Nothing inside BAS calls it by name. The disk reader is a caller that has not been found. `FUN_12c8_0ef8` sees a structure that is already not the disk record. The step between those two forms is the open problem.

## What was closed

- `FUN_1028_2680` is a filter registrar, not the record reader.
- `FUN_1008_2dc7` is the math dispatcher, not the record reader. The same path is `FUN_1008_2d31` in a later listing. It handles `+ - * /` and `abs`, `sqrt`, `log`, `exp`, `sin`, `cos`, `atan`, `asin`, `acos`.
- `TB80RTM` has no `14 00 00` reader and no named file open. `WM_PAINT` calls `CLIENTTOPAGE`, then ordinal 26, `CDBPAINTCLIENT`. The painters are in BAS.
- Sampled BAS segments `1018`, `1278`, `1478`, `14b8`, `1508`, `10d0`, `1030`, `14a8`, `1160`, `1070` do not contain that reader either. Absence from the HTML listing is not absence from the binary. The listing has `??` regions. A candidate closed only on the HTML is closed for the disassembled part.
- The polygon type table is built at runtime. A static search of the image will not find it.
- An ascending word table inside a page, such as the 27 words at page `+0x8C3` on P1170, is a content index into a `14 00 00 83` blob. It is not a Group. A Group is its own object and has its own member list.

## Geometry the papers added

Content rectangles are bounds-only. In the page blob the tail is four twip words, a zero dword, a fill dword, then `01 00 00 04`. Screen position is twips / 15. P1040 is 28 pin boxes and 2 body boxes. The pin tip is not stored as an 11-point list. Paint expands it. A later count on `9e954d01.tbk` found 961 of the marker.

Polygon kind `04 00` is unchanged: count at `+0x1A`, points at `+0x22`.

An arc on disk is type `0x11`, four twip pairs at `+0x25`. No page record has been matched to it, and the angles are not located.

P420 curve points sit near page `+0xA13`. The control structure is not known. Type id `0x05C7` does not occur in the page.

Pictures that are already Windows BMPs can be carved. A match against one TBX export paired 67 markers with 72 bitmaps. The widget still does not name the bitmap. Compressed pictures go through `TB80BMP` ordinal 3 and stop at the far call `0x1FCD`.

## Paint and chrome, from the RTM listing

`GETDLGITEM` is called most often with control id `0x65` (101), 55 hits. `GETWINDOWLONG` is called most often with index 10, 196 hits. `FUN_1068_0098` is `GLOBALALLOC` with a retry on failure. `FUN_1068_0000` is the dialog helper. `SENDMESSAGE` (321 hits) and `LSTRLEN` (282 hits) have mangled arguments. Those want a fresh decompile, not another reading of the same listing.

BAS segment `1150` builds the palette (`CREATEPALETTE`, `SELECTPALETTE`, `REALIZEPALETTE`). Field text is `DRAWTEXT` from `param_5+0x4A`, `+0x4C`, and `+0x50`. Segment `1018` creates and deletes pens, brushes, and bitmaps. Who owns them is open.

## System books, as the papers left them

`TB80UTL` holds the type names: ComboBox, Stage, Picture, Polygon, Field, Button, Page, Book. The `.sbk` files carry menu resources. `nc81int.dll` and `nc81rec.dll` were decompiled as the live handlers. The papers did not find plain-text OpenScript in the `.sbk` files.

A later reader found compressed handler streams in system books, stored as keyword opcodes (`80 81` for `to handle`) rather than the words. That does not contradict a search that was looking for the text. It does mean "no script in the system book" is too strong. What those streams do when a lesson runs has not been traced. `initializebase`, `initializerecs`, and `initializetest` are still names, not a call log. `toolbook.lst` is the load list. The order has not been watched.

## How a page is indexed

`80 65` records are the pages. A TBX page can name a background by an id, such as 23, that does not appear as a word or a dword in the matching binary page. The link is indirect. Parent and z-order are not in the page record that has been decoded.

`nida81.tbk` has 100 `buttonClick` handlers whose names are still text. `9e954d01.tbk` has 129 pages.

## Ghidra

NE segment numbers do not match Ghidra segment names. The table is `maps/rtm-ne-to-ghidra.md`. Segment 1 is `1000`, segment 2 is `1008`, and the step is usually 8, with gaps.

The HTML export is not a complete disassembly. Do not close a function because it is missing from that export.

Two Script Manager passes force the listing to finish. One starts at `C8` sites. The next walks undefined bytes and creates a function at `55 8B EC`, at the Win16 export prolog `45 55 8B EC 1E 8E D8`, at the byte after `C3` or `CB`, and at every NE entry that has no function.
