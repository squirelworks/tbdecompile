# Theories of Operation for the Open Gaps

Scaffolding for the pieces whose ToolBook implementation has not been recovered. Each theory is a working model that fits the evidence already in hand and can be tested or replaced. None of these are confirmed.

## 1. Disk record reader (caller of CDBSENDCREATE)

**What we know**
- `CDBSENDCREATE` receives bounds already formed and writes them via `FUN_12c8_0ef8`.
- On disk, widgets are `14 00 00` chunks inside the page.
- Content rectangles and polygons have been parsed directly from those chunks (bounds, fill, point count, twip pairs).
- No static search of the decompiled HTML has found a walker that matches the `14 00 00` signature and then calls the create path.

**Theory**
The reader is a page-load function that walks the page's nested chunks by length fields rather than by searching for the signature. It classifies each chunk by a type byte or by a property-id table, extracts the bounds (or computes them from vertices), builds a temporary structure, and calls `CDBSENDCREATE`. The signature is only a marker for tools; the runtime trusts the length-prefixed layout. That is why the reader does not contain the literal bytes `14 00 00` in a comparison.

**Test**
Break on `CDBFILEOPEN` (BAS ordinal 8) after a page is requested, then break on `CDBSENDCREATE` and compare the source buffer address on the stack with the page blob. Alternatively, force disassembly of the remaining undefined regions that start with `ENTER` and look for a loop that reads a length word and then copies four words of bounds.

## 2. Curve control structure (P420)

**What we know**
- P420 contains point runs inside a large record at page+0xA13.
- A naïve render of those points produces a tangle, not a flame.
- TBX expands the flame to three 96-point IrregularPolygons.
- Curve type id is `0x05C7` in the system-book type table; that id has not been found in the page.

**Theory**
The points are stored as multiple independent pen strokes, not as a single polygon. Each stroke has its own length or terminator. The "tangle" is the result of concatenating strokes that should be drawn separately. The type id is not stored in the page because the object is created as a generic vector object and the stroke list is a property (possibly `0x4050` or a private property) rather than a typed record. The TBX Vertices lists are the expanded form of those strokes.

**Test**
Re-parse the +0xA13 record looking for repeated length prefixes or zero terminators between point groups. Compare the resulting stroke lengths to the three 96-point groups in the TBX export. A live break on the polyline/polygon painter while P420 is visible should show successive calls with different point counts.

## 3. Arc angles and disk layout

**What we know**
- Live arc object is type `0x11`.
- Geometry is four twip pairs at object+0x25, +0x29, +0x2D, +0x31 plus the bounding box at +0x0F.
- Fill color at +0x18.
- No matching `14 00 00` pattern has been tied to an arc on disk.
- ToolBook never calls GDI `PIE`; pie wedges are computed from the same layout.

**Theory**
Arc angles are not stored as degrees. They are stored as the four endpoint pairs (start and end of each ray). The painter converts those pairs into the GDI `ARC` arguments. On disk the arc is either a bounds-only record whose type byte selects the arc path, or it is a property block inside a generic draw object. The type `0x11` is assigned at create time by the reader, not written as a literal in the page.

**Test**
Locate a page that TBX identifies as containing an Arc. Dump the corresponding binary page and look for a bounds-only record whose size and following property block match the live object layout after the create path. Alternatively, break on the arc painter and walk one frame up to the type dispatcher to see the source record pointer.

## 4. Picture-id binding

**What we know**
- BMPs are embedded in the book and can be carved.
- TB80BMP ordinal 3 is the reader that produces a DIB.
- No widget field that holds a picture id has been identified.
- Picture objects exist in the type table.

**Theory**
A picture widget stores a resource id or an offset into the book's resource area as a property (likely in the 0x4000 range). At paint time the property is resolved through TB80BMP, which returns a bitmap handle stored in the object (object+0x3B has been observed as a GDI handle). The id is not a simple integer next to the bounds; it is a property that the reader installs when it processes the chunk.

**Test**
Break on TB80BMP ordinal 3 while a page with a known picture is painted. The caller should be a BAS paint function. Walk the stack to the object pointer and inspect the property area for a value that matches a resource id or file offset of a carved BMP.

## 5. Background, parent, and z-order

**What we know**
- TBX pages can name a background by an id that does not appear as a word or dword in the matching binary page.
- Parent and z-order are not in the page record that has been decoded.
- The page content blob contains an offset table (observed on P1170).

**Theory**
Background linkage is stored in the page's property block or in a separate index that is built at load time. The id is resolved through a book-level table, not stored inline. Parent and z-order are either implicit in the order of the nested chunks or stored as short integers in the property block that the reader copies into the object. The offset table is a directory of widget starts inside the content blob, not a group.

**Test**
Compare a TBX page that references a background with its binary page. Look for a property whose value equals the background id after the page has been loaded (break after `CDBSENDCREATE` for the page object and dump its property area). For z-order, paint a page and record the order of painter calls; that order should match either the chunk order or a small integer field.

## 6. System-book initialize sequence

**What we know**
- Lessons call `initializebase`, `initializerecs`, `initializetest`, `openSession`, `gotoPageList`.
- These names appear in OpenScript and resolve either to handlers in `nida81.tbk` or to exports in `nc81int.dll` / `nc81rec.dll`.
- `toolbook.lst` is the load list.
- Removing the system books breaks resize, splash, and menu.

**Theory**
The initialize calls are ordinary OpenScript `send` operations that land in `nida81.tbk` handlers. Those handlers then call the DLL exports. The load order in `toolbook.lst` determines which system books are present before the first lesson page runs. The splash and resize behavior are side effects of the base system book having been loaded and having registered window procedures or property handlers.

**Test**
Break on the OpenScript send path (or on the known handler entry in `nida81.tbk`) when a lesson starts. Log the sequence of sends and the subsequent DLL calls. Compare that log with the order of names in `toolbook.lst`.

## 7. Stroke color, pen width, palette, and GDI object lifetime

**What we know**
- Fill color is present in the disk records and in the live object.
- Stroke color and pen width have not been located.
- Segment 1150 builds the palette.
- Segment 1018 creates and deletes pens, brushes, and bitmaps.
- Object+0x3B has been observed as a GDI handle.

**Theory**
Stroke color and pen width are properties that default to the fill color and a unit width when absent. They are installed by the same reader that handles fill. The palette is a book-level or page-level object created once and selected into the DC. Pens and brushes are created on demand by the painters and deleted by the same segment that created them, or by a cleanup pass when the page is left. Object+0x3B holds the currently selected GDI object for that widget.

**Test**
Break on `CREATEPEN` / `CREATEBRUSH` while a page with known stroke attributes is painted. The caller should be near the painters. Dump the object to see whether stroke values are stored adjacent to the fill color.

## Summary of the scaffolding

| Gap | Working model | Next concrete step |
|-----|---------------|--------------------|
| Disk reader | Length-prefixed chunk walker that calls CDBSENDCREATE | Break on ordinal 8 then ordinal 51; compare buffers |
| Curves | Multiple independent strokes inside one record | Re-parse +0xA13 for length prefixes; compare to TBX |
| Arcs | Endpoint pairs, type assigned at create | Match TBX Arc page to binary; break on arc painter |
| Pictures | Property-held resource id resolved by TB80BMP | Break on BMP ordinal 3; walk to object |
| Background / z-order | Indirect id + chunk order or property | Dump page object properties after create |
| Initialize sequence | OpenScript sends into nida81 then DLLs | Log sends at lesson start |
| Stroke / palette | Properties + segment 1150/1018 | Break on CREATEPEN while painting |

These models are sufficient to keep implementation work moving. Each can be confirmed or discarded by one targeted SoftICE session or by one additional parse of an already-extracted page.
