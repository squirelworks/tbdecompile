**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# BAS HTML Listing Extracts — CDB / Paint / Create

> Trail, 2026-10-16. Superseded. Chapter 4. Extracts that treat ordinal 51 as runtime are superseded. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: `/workspace/attachments/TB80BAS.DLL.html` (and variants)

## CDB-named functions (top by mention count)

| Count | Name |
|------:|------|
| 331 | CDBPAINTELLIPSE |
| 250 | CDBSETPLERR |
| 185 | CDBSETSCRIPTPROPERTY |
| 181 | CDBNEWOBJECT |
| 134 | CDBDELETEOBJECTVALUE |
| 126 | CDBVALUEGRAPHICFROMSTRING |
| 123 | CDBPAINTROUNDRECT |
| 121 | CDBVALUE |
| 120 | CDBGETVALUEEX |
| 114 | CDBCOPYOBJECTPROPERTIESVALUE |
| 98 | CDBFILESAVEAS |
| 96 | CDBVALUELAYERFROMSTRBOOK |
| 89 | CDBSENDVALUEEX |
| 88 | CDBSETPROPERTY |
| 85 | CDBDEREFVALUE |
| 84 | CDBSEARCHINIT / CDBRESOURCEUSEDBY |
| 83 | CDBSCALETWIPSTOSCREEN |
| 80 | CDBSYNCSCREENS |
| 75 | CDBSETUPPAINTRECT |
| 69 | CDBSENDCREATE |
| 67 | CDBSETVALUEEX / CDBSENDSELECT / CDBPAINTARCALT |
| 45 | CDBPAINTRECTANGLE |
| 41 | CDBPAINTARC |

Full unique CDB* set is larger; the above are the highest-frequency names in the listing.

## Paint functions (CDBPAINT*)

| Count | Name | Notes |
|------:|------|-------|
| 331 | CDBPAINTELLIPSE | |
| 123 | CDBPAINTROUNDRECT | |
| 67 | CDBPAINTARCALT | |
| 45 | CDBPAINTRECTANGLE | |
| 41 | CDBPAINTARC | |
| 33 | CDBPAINTCLIENT | |
| 21 | CDBPAINTROUNDRECTALT | |
| 16 | CDBPAINTROUNDRECTALT2 | |
| 11 | CDBPAINTPOLYLINE | |
| 10 | CDBPAINTELLIPSEALT | |
| 5 | CDBPAINTPOLYGON | Matches known segment 0x82 / 1408:0376 |
| 3 | CDBPAINTARC2 | |

## Confirmed entry points from listing

- **CDBPAINTPOLYGON**: 1408:0376 (segment 130 in the HTML numbering)
- **CDBSCALETWIPSTOSCREEN**: 1008:01dd
- **CDBPAINTARC** and **CDBPAINTRECTANGLE** appear in the 1020 segment range (cross-calls between them)

## Create path reminder

`CDBSENDCREATE` (ordinal 51, 12c8:00bc) → `FUN_12c8_0850` → `FUN_12c8_0e32` → `FUN_12c8_0ef8`.  
Type dispatch and bounds write happen inside `0ef8`. The `14 00 00` record parser remains upstream.

## UTL cross-check (from TB80UTL.DLL.html)

Object kind strings present: Button (30), Field (11), Polygon (5), Rectangle (3), Group (3), IrregularPolygon, Ellipse, Curve, ComboBox.

These match the classification table previously extracted from the raw DLL.

## Next possible cuts

- Full XREF dump for `CDBSENDCREATE` and the paint functions
- Segment layout table for BAS (all CodeN: entries)
- Same extract for RTM, UTL, VBX, RCR
- nida81.tbk.html handler surface

All HTML listings are under `/workspace/attachments/`.
