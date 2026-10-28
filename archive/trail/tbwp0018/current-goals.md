# Current research goals

> Trail, 2026-10-16. Chapter 10.6. Order of work. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Graphics

| Goal | Status | Notes |
|------|--------|-------|
| Polygon | Solved | kind=0400, count at +0x1A, points at +0x22 |
| Content rectangles | Solved | bounds at -16, fill at -4, marker 01 00 00 04 |
| Arc | Layout known | type 0x11, four twip pairs at +0x25. No on-disk match yet. Angles not located |
| Curve | Points found | P420 +0xA13 has real points (~400-500). Control structure unknown. Type ID 0x05C7 not in page |
| Picture binding | Partial | BMPs carved. 67 markers matched to 72 TBX bitmaps. Resource ID to widget binding open |
| Palette | Open | BAS segment 1150 builds the palette. 8bpp BMPs need it |
| Field text paint | Open | DRAWTEXT reads from param_5+0x4a/+0x4c/+0x50 |
| GDI resource lifetime | Open | Who creates pens/brushes, where they live, who deletes them |
| Per-pin position | Open | Index at +0x52 not yet applied. Pins overlap because records share identical point bytes |
| Stroke/line color | Open | Fill is extracted. Stroke color and pen width not yet located |

## OpenScript

| Goal | Status | Notes |
|------|--------|-------|
| Common subset | Works | goto, send, assign, if/else, step |
| Expression evaluator | Partial | + - * / and abs/sqrt/log/exp/sin/cos/atan/asin/acos. Falls back to original string |
| Token map gaps | Open | Less common opcodes. Needs a compile+expand ground truth from Instructor 8 |
| High-byte back-refs | Fixed | 0xC0-0xFF copy from compressed input stream |
| System book handlers | Done | nc81int.dll / nc81rec.dll decompiled. No OpenScript in .sbk files |
| nida81 handlers | Done | 100 buttonClick handlers extracted |

## System books

| Goal | Status | Notes |
|------|--------|-------|
| Type table | Done | UTL holds ComboBox, Stage, Picture, Polygon, Field, Button, Page, Book |
| Menu resources | Done | System .sbk files are resource containers |
| Live handlers | Done | nc81int.dll / nc81rec.dll decompiled |
| Runtime contract | Open | What initializebase / initializerecs / initializetest actually invoke |
| System book load order | Open | toolbook.lst is the load list. Actual order and dependencies not traced |

## Object struct

| Offset | Known | Open |
|--------|-------|------|
| +0x0f | Bounds (left, top, right, bottom) | |
| +0x17/+0x19/+0x1b/+0x1d | Property expansion copies | Source offsets do not match disk 14 00 00 record |
| +0x1f | BitBlt raster op flag | |
| +0x30 | Point count | |
| +0x32 | Point array far pointer | |
| +0x3b | GDI handle | |
| +0x52 | Per-pin position index | Not yet applied |
| +0x76 | Struct size | |
| -2 | Type byte | 0x11 = arc. Other types not mapped |

## Page / background index

| Goal | Status | Notes |
|------|--------|-------|
| Page markers | Done | 80 65 records are pages |
| Background link | Open | TBX P10213 references Background id 23. Binary page at 0x21db85 has no word/dword 23. Link is indirect |
| Parent / z-order | Open | Not in the page record that has been decoded |
| Page count | Done | 129 pages in 9e954d01.tbk |

## Property expansion

| Goal | Status | Notes |
|------|--------|-------|
| Disk form | Known | 14 00 00 01 + six words after the name |
| Memory form | Partial | One SoftICE dump showed 14 00 00 11. Not confirmed as load-time mutation |
| Expansion step | Open | FUN_12c8_0ef8 copies source+0x3e/+0x40/+0x42/+0x44 to object+0x17/+0x19/+0x1b/+0x1d. Disk record does not match those offsets |
| Bounds write | Open | Bounds appear at object+0xF. Write site not found |

## Decompile polish

| Item | Status | Notes |
|------|--------|-------|
| SENDMESSAGE args | Mangled | 321 hits. Message IDs not recovered. Bookmark for re-decompile |
| LSTRLEN args | Mangled | 282 hits. String pointers not recovered. Bookmark for re-decompile |
| GETDLGITEM control IDs | Partial | Top ID is 0x65 (101, 55 hits) |
| GETWINDOWLONG indices | Partial | Top index is 10 (196 hits) |
| Undisassembled regions | Open | 165 runs of >20 ?? lines in BAS HTML. 108 start with ENTER. ForceDisassembleC8.java written |
| Entry table | Done | Ghidra NE loader fix applied. Entry segment bytes >= 128 rewritten |

## Naming

| Module | Confirmed | Nameable | Notes |
|--------|-----------|----------|-------|
| BAS | 20 | ~646 | PaintPolygon, ScaleTwips, SetProperty, SetPointArray, PaintArc |
| RTM | 8 | ~870 | Thin wrappers: BEGINPAINT, ENDPAINT, CREATEWINDOW |
| BMP | 11 | ~26% | CreateDibBitmap, BitBltBmp, Lz77Expand |
| CMP | 8 | ~5.6% | LoadCompilerResource, ExpandTextCore |
| UTL | 7 | ~41% | Object type table |
| Others | 58 | varies | MM, RCR, FLT, NET, JPG, VBX, W16, LNL |
| Total | 112 | ~17.5% | 10,991 unique functions across 8 modules |

## Not in scope (for now)

- 14 00 00 record reader (debugging path)
- Authorship / CMP full reimplementation (planned milestone)
- Non-NIDA ToolBook features
- ActiveX / VBX / OLE beyond what NIDA uses
