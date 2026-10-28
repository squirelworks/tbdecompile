# Appendix B — Architecture and Gaps

What is known, what is known to exist, and where the gaps are.

**Date:** 16 October 2026

**Status:** This appendix replaces the 15 October 2026 architecture appendix. The diagrams in that file that put `CDBSENDCREATE` between the page walk and the live object described a real function in the wrong place. Those drawings are not the runtime path.

This file is the architecture appendix only. The narrative record is the contents volume. Export maps, numeric tables, and address maps are their own appendices. Nothing in those files is repeated here in order to make this one longer.

## How to read this

`[+]` is a recovered fact. A later observation would have to contradict the evidence.

`[?]` is a confirmed gap. The thing exists. The function or the offset does not have a name yet.

`[×]` was drawn in the 15 October appendix, or in an older operating note, and a later trace closed it. It is not a target.

## 1. Overall architecture

ToolBook II 8.1 is a 16-bit NE book engine (`TB80RTM.EXE`) with a 32-bit launcher (`TB80RUN.EXE`) and a satellite DLL set.

```
TB80RUN.EXE (32-bit)
        |
        | WinExec
        v
TB80NET.EXE (16-bit)
        |
        v
TB80RTM.EXE                         NE book engine
        loads TB80BAS.DLL           objects, paint, properties
        loads TB80CMP.DLL           OpenScript compile / expand
        loads TB80BMP.DLL           DIB / picture
        loads TB80W16.DLL           DoCmd bus, thunks
        loads TB80UTL.DLL           object type table
        loads system books          nc81base/recs/test/trnr.sbk
                                    tb80r.sbk, nida81.tbk
        |
        v
page records in memory              80 65
        |
        v
[?] record reader                   length-prefixed walk
                                    does not call ordinal 51
        |
        v
live objects                        bounds at +0x0F
        |
        v
WM_PAINT
        |
        v
CLIENTTOPAGE -> CDBPAINTCLIENT      BAS ordinal 26
        |
        v
BAS painters -> GDI
```

`[+]` `TB80RTM` is the engine. `TB80BAS` owns object storage and paint. `TB80UTL` owns the type-name table.

`[×]` The 15 October arrow from the unnamed reader into `CDBSENDCREATE`. Ordinal 51 creates or rewrites objects from the Instructor UI. A lesson open does not call it.

`[?]` The function that walks a page blob and builds objects. It sits in BAS after `CDBFILEOPEN` and before the first paint. It has no name.

## 2. Book open path

```
Tbload / TB80RUN
        |
        v
find ZZZTBKBOOKLOC                  file offset of the book data
        |
        v
JBO signature check                 virtual method, not a literal compare
        |
        v
[?] page structure allocation       virtual method
        |
        v
CDBFILEOPEN                         BAS ordinal 8
        |
        v
page objects appear                 80 65 records
        |
        v
[?] walk nested chunks              length-prefixed
                                    a literal compare to 14 00 00 is not required
        |
        v
live object                         bounds at +0x0F
        |
        v
paint                               ordinal 26, then the BAS painters
```

`[+]` `ZZZTBKBOOKLOC` is searched by Tbload. JBO is checked. `CDBFILEOPEN` is named. SoftICE and WDW both reached `OBJFILEOPEN` and the buffered read in `FUN_1160_03de`. When the buffer satisfies the request, the raw DOS path at offset `04F3` is skipped.

`[×]` `CDBSENDCREATE` (ordinal 51) as the step that turns those chunks into objects. The W16, UTL, and BAS export traces do not show it on book open. Do not break on ordinal 51 to find the reader. The stop fires when Instructor creates or rewrites an object.

`[?]` The virtual method that allocates page structures, and the walker that runs after `CDBFILEOPEN`.

## 3. Author create path

This tree is recovered. It is not the reader.

```
CDBSENDCREATE (12c8:00bc, ordinal 51)
        |
        +-- param_5 == 0x1014 / 0x1015 --> FUN_12c8_0850
        |                                      |
        |                                      v
        |                                 FUN_12c8_0e32   allocator
        |                                      |
        |                                      v
        |                                 FUN_12c8_0ef8   field copier
        |                                      |
        |                                      v
        |                                 object+0x0F = bounds
        |
        +-- param_5 == 0x1021 / 0x1022 --> FUN_12c8_0a86
        +-- param_5 == 0x3018-0x301b   --> CDBCHECKBOUNDDTL + FUN_12c8_0e08
        +-- else                       --> ordinal 115
```

`[+]` A live object is `0x76` bytes. Bounds are four words at `+0x0F`, `+0x11`, `+0x13`, `+0x15`, in twips.

`[+]` `FUN_12c8_0ef8` copies source `+0x3E` / `+0x40` / `+0x42` / `+0x44` to object `+0x17` / `+0x19` / `+0x1B` / `+0x1D`.

`[+]` Nothing inside BAS calls `CDBSENDCREATE` by name. One external thunk, from `FUN_13d0_0822`, reaches ordinal 51. That caller tests author-UI bytes and stores coordinates around object `+0x638`.

`[?]` The source structure `FUN_12c8_0ef8` reads is not the on-disk `14 00 00` record. An expansion step sits between them on the author path. That step is still not the runtime reader.

## 4. Object layout

| Offset | Size | Meaning | Status |
|---|---|---|---|
| `-2` | word | Type. `0x11` is an arc. Other type bytes are not mapped. | `[+]` for `0x11` only |
| `+0x0F` | four words | Left, top, right, bottom, twips | `[+]` |
| `+0x17` | four words | Copied by `FUN_12c8_0ef8` from a source structure | `[+]` as a copy |
| `+0x1F` | byte | BitBlt raster-op select | `[+]` |
| `+0x25` | pairs | Arc geometry, four twip pairs | `[+]` |
| `+0x30` | word | Polygon point count | `[+]` |
| `+0x32` | far ptr | Polygon point array, 4 bytes per point, stored twips | `[+]` |
| `+0x3B` | word | GDI handle | `[+]` |
| `+0x52` | word | Per-pin index. Not applied by the current clean-room draw. | `[+]` that the field exists |
| unknown |  | Picture resource id | `[?]` |
| unknown |  | Script / handler pointer | `[?]` |
| unknown |  | Parent / group link | `[?]` |

`ScaleTwipsToScreen` is `FUN_1008_01dd`, BAS segment 2 offset `0x1DD`. With `DS:01A6` and `DS:01A8` at 96, screen pixels are stored twips / 15, which is `(stored * 96 + 720) / 1440`.

## 5. Paint path

```
WM_PAINT (RTM)
        |
        v
CLIENTTOPAGE
        |
        v
CDBPAINTCLIENT                      BAS ordinal 26
        |
        v
type dispatcher                     BAS, built at load or by relocation
        |
        +-- polygon    PaintPolygon     1408:0376
        |                 count at +0x30, points at +0x32
        |                 ScaleTwipsToScreen, then GDI POLYGON
        |
        +-- polyline   PaintPolyline    13e8:00E6
        |
        +-- rectangle  PaintRectangle   1020:03E4 and FUN_1410_0066
        |                 bounds at +0x0F, then GDI RECTANGLE
        |
        +-- arc        PaintArc         segment 0x7B, helpers at 10A0
        |                 four twip pairs at +0x25
        |
        +-- ellipse    PaintEllipse     1230:2F1C and an alt
        |
        +-- roundrect  PaintRoundRect   1230:2278 and alts
        |
        +-- curve      [?] stroke walker
        |                 points exist; control structure unknown
        |
        +-- picture    [?] property to TB80BMP ordinal 3, then a DIB
                          +0x3B has been observed as a GDI handle
```

`[+]` ToolBook does not call `GDI!PIE`. Pie wedges are computed and filled with the arc geometry.

`[+]` A diagram bracket is not stored as points. BAS segment `0x5B` computes four polyline points from the bounds.

`[?]` The curve control structure, and the property that holds a picture id.

## 6. On-disk records

A page object starts `80 65 00 05 00 02 02`. The page name is a 32-byte field. Widgets are not separate top-level objects. They are length-prefixed chunks nested in the page, beginning `14 00 00`.

Polygon, kind `04 00`:

- Fill dword at `+4`.
- `+0x0C` = `04 00`.
- Point count word at `+0x1A`.
- Twip pairs at `+0x22`.
- Screen = twips / 15.

`9e954d01.tbk` has 96 of those records on 13 pages. P430 has 22.

A content rectangle is bounds-only. The tail is four twip words, a zero dword, a fill dword, then `01 00 00 04`. The same book has 961 of that marker. The pin tip is computed at paint. The TBX export writes the expanded Vertices. Matching a Vertices list back to the binary means matching the bounding box.

`[+]` Polygons and content rectangles have been parsed from the page blob.

`[?]` The runtime reader that turns these chunks into objects is not the parser the clean-room tools use. It has not been located. A static search has not found the bytes `14 00 00` used as a compare against a far pointer that then builds an object. The working model is that the reader trusts the length prefix and does not search for the marker. That model is not proven.

## 7. OpenScript path

```
on disk: handler bytecode in the page blob
        |
        v
resource 0x77                       keyword offset table
        |
        v
high bytes and back-references      whitespace, repeats, copies
        |
        v
source text                         "go to page", "send next", ...
        |
        v
[?] expression evaluator            FUN_1008_2d31 is the math path
        |
        v
runtime dispatch                    goto, send, assign, if, step
```

`[+]` The keyword table is resource `0x77`. Back-references `0xC0`–`0xFF` copy from the compressed input stream. An earlier decoder copied those bytes from the output and produced the wrong words. That decoder is closed.

`[+]` The common subset (`go to page`, `send next` / `previous`, basic conditionals, system properties) decodes. `tb80r.sbk` uses the same bytecode. There the handler-name prefix is compressed as well. Thirty-three handlers have been extracted.

`[?]` Full expression evaluation, and the compile-time token map, are only partly recovered.

## 8. System books

| File | What it is |
|---|---|
| `nc81base.sbk` | Resource container. Object-type name table. No decoded `to handle` text. |
| `nc81recs.sbk` | Resource container. No decoded `to handle` text. |
| `nc81test.sbk` | Resource container. No decoded `to handle` text. |
| `nc81trnr.sbk` | Resource container. No decoded `to handle` text. |
| `tb80r.sbk` | Same container. 33 compressed handlers. Not "no script at all." |
| `nida81.tbk` | A book. 43 objects, pages `P20000`–`P22130`, 100 `buttonClick` handlers. |
| `nc81int.dll` | 47 trainer / comms exports. |
| `nc81rec.dll` | Session recording exports. |

`[+]` The four `nc81*.sbk` files do not hold the lesson logic. Lessons call `initializebase`, `initializerecs`, `initializetest`, `openSession`, and `gotoPageList`. Those names resolve to `nida81.tbk` or to the two DLL export sets.

`[×]` The 15 October sentence that all system books are scriptless resource containers and that the logic lives only in the DLLs. It is too strong for `tb80r.sbk`, and it skips `nida81.tbk`.

`[?]` What the `tb80r.sbk` streams do when a lesson runs. The exact handoff from a lesson script into `nc81int` / `nc81rec` is only partly traced.

## 9. Confirmed gaps

These are the places further debugger work is expected to pay off. The "where to look" column is the current one. A 15 October instruction that said to break on `CDBSENDCREATE` and walk the stack is not on this list.

| Gap | What exists | Where to look |
|---|---|---|
| Page-blob walker | Builds objects after `CDBFILEOPEN`, before the first paint | `TB80BAS@CDBFILEOPEN` on a lesson open, then resume. Then `CDBCREATEPAGEREF` or `CDBSETVALUEEX`. |
| Disk record to live object | The `14 00 00` chunk and the `0x76`-byte object are different shapes | When an object exists, dump `+0x0F` and the page offset it came from. |
| Curve strokes | P420 point runs. Three 96-point red polygons in the TBX. | The on-disk control structure at the page. Not another W16 or UTL export pass. |
| Picture id | TB80BMP ordinal 3 reads a DIB | Break on that ordinal. Inspect the object. |
| Script pointer | Handlers live in the page blob as bytecode | Script dispatch, not ordinal 51. |
| Parent / group | Relative bounds become absolute. The P1170 bracket was computed from a parent. | `CLIENTTOPAGE` or the bounds setter. The parent offset is not in the decoded page record. |
| Expression eval | Math beyond the FPU path in `FUN_1008_2d31` | Compile and expand a short script. |

Closed, so they are not searched again as the reader: `CDBCHUNK*` (text walkers), `VALUENEWLONG` (a constructor), `OBJFILEOPEN` (downstream of the reader), `TB80RTM` (no named file open), the OpenScript math switch, and the filter registrar whose `0x14` is a type-code limit.

## 10. Working model of the missing reader

Not recovered. Fits the evidence. Not a listing.

```
function LoadPage(page_blob):
    offset = 0
    while offset < length(page_blob):
        chunk = page_blob[offset:]
        # length-prefixed. A search for the bytes 14 00 00 is not required.
        if not length_prefixed(chunk):
            break
        if kind(chunk) == 0x0400:
            obj = make_object()          # not CDBSENDCREATE
            set_bounds(obj, bounds_of(chunk))
            if has_points(chunk):
                set_point_array(obj, count_at_+0x1A, pairs_at_+0x22)
            set_fill(obj, dword_at_+4)
        elif is_bounds_only_rect(chunk):
            obj = make_object()
            set_bounds(obj, four_twip_words(chunk))
            # the pin tip is computed later, at paint
        elif is_picture(chunk):
            obj = make_object()          # picture id property is unnamed
        elif is_script(chunk):
            attach_handler(obj, chunk.bytecode)
        offset += chunk.length
    return objects
```

The step that has a name on the author side (`CDBSENDCREATE`, then `FUN_12c8_0ef8`) is not this function. Calling the author path from this model was the 15 October mistake.

## 11. What this means for a clean-room reader

A modern reader does not need the unnamed function. It needs the disk layout, which is partly recovered.

`[+]` Page objects are findable by the `80 65` marker. `9e954d01.tbk` has 129 of them.

`[+]` Polygons and content rectangles can be drawn from the nested chunks. Where the binary stores bounds, paint or the TBX export expands the tip.

`[+]` OpenScript handlers can be expanded to source, using the input-stream back-reference rule.

`[+]` The `nc81*.sbk` files supply type names and menus. `nida81.tbk` supplies the shell.

`[?]` Absolute position of nested objects, picture binding, and curve stroke order still need either the missing reader or a theory that matches the TBX expansion.

The `[?]` rows are the research targets. The `[+]` rows are what a clean-room implementation can already stand on. The `[×]` rows are not targets.
