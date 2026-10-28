**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Ghidra research list — graphics and page layout

> Trail, 2026-10-16. Superseded. Chapters 10 and 17. Create-path items in that list are superseded. If this file and `TBdecompile/record/` disagree, the record wins.

From TB80BAS.DLL.c (Toolbook/_decompiles/) and the 20261012 notes.
HTML export would help for XREF chasing; the .c is enough for the first pass.

## 1. Bounds: disk record → object+0xF

**Known**
- `CDBSENDCREATE` (12c8:00bc) receives bounds as parameters.
- Calls `FUN_12c8_0850` → `FUN_12c8_0e32` → `FUN_12c8_0ef8`.
- `FUN_12c8_0ef8` writes bounds to the object (param_7) at +0xF / +0x11.
  Two write sites: lines 150–151 (from DAT_1630_01fe) and 200–201 / 213–214 (from param_2).
- Object is 0x76 bytes. Bounds live at +0xF / +0x11 / +0x13 / +0x15.
- Type dispatch on param_5: 0x1014/0x1015 = new object; 0x3018–0x301b = bounds-checked.

**Open**
- Who reads the `14 00 00` record and passes the four twips into `CDBSENDCREATE`?
- That caller is not in the current BAS decompile under a named export.
- Next: XREF on `CDBSENDCREATE` in the RTM or Tbload path, or search BAS for the signature bytes.

## 2. Polygon / IrregularPolygon points

**Known**
- On-disk: `14 00 00` subtype-0, `+0x0c = 04 00`, fill dword at +4, count at +0x1A, pairs at +0x22.
- Runtime: `FUN_1408_00d8` (SetPointArray, ~line 169871) is the 0x4050 setter.
  Stores count at object+0x30, allocates count*4 via `OBJNEWNEAR` into +0x32, copies the pairs.
  Special-cases 0x4034 (vertices) by forwarding to `FUN_12d0_03ec`.
- Painter: `FUN_1408_0376` (PaintPolygon) reads count at +0x30, scales via `FUN_1008_01dd`, calls `GDI!POLYGON`.
- 96 such records on 13 pages in 9e954d01; P430 has 22.

**Open**
- How the on-disk pairs become the 0x4050 property data. Is it a direct copy or a transform?
- Per-pin offset (the +0x52 index that makes pins not overlap).

## 3. Curve (P420 flame)

**Known**
- Points exist in the page blob at +0xA13. Screen ~400–500.
- Type id 0x05C7 is in nc81base.sbk. Not found as a named record in the page.
- Current render is a tangle — order or grouping is wrong.

**Open**
- Header / count / segment breaks inside the +0xA13 record.
- Whether the points are absolute or relative to a parent bounds.

## 4. Arc / Pie

**Known**
- Live object type 0x11. Four twip pairs at +0x25/+0x27, +0x29/+0x2B, +0x2D/+0x2F, +0x31/+0x33.
- Fill at +0x18. Painter is BAS segment 0x7B.
- No `GDI!PIE` call. Pie is computed via `GDIELLIPSEPOINTFROMANGLE` then filled as a wedge.
- Property 0x4123 is the angle setter.

**Open**
- Matching `14 00 00` pattern on disk. Not yet tied.

## 5. Picture / DIB binding

**Known**
- 641 BMPs carved from the course books.
- `CDBCREATEGRAPHICREF` exists (export, ~line 37711). Takes an id and returns a ref.
- TB80BMP ordinal 3 is the DIB reader. Proxy already logs it.
- String `DIBDESC` appears in BAS.

**Open**
- Which field in the page widget holds the picture id.
- Whether the id is a resource index, a file offset, or a name.

## 6. Computed shapes (brackets, lines)

**Known**
- Segment 0x5B builds a bracket from the object bounds (not stored points).
- SoftICE: GDI!POLYLINE with 4 points computed from bounds at object+0x0E.

**Open**
- Once bounds are recovered, these should fall out. No extra disk data needed.

## 7. OpenScript → layout

**Known**
- Handlers are decoded. `go to page`, `send`, `set ... to` are readable.
- Property ids: bounds=0x4004, text=0x402e, script=0x4023, vertices=0x4034, idNumber=0x4015.
- `FUN_1058_0a98` is the per-type property registrar (15 types).

**Open**
- Which handlers set bounds or vertices at runtime (vs. stored in the page blob).
- Whether a page can move widgets after load via OpenScript.

## HTML export

An HTML decompile (Ghidra Export → HTML) would make XREF chasing easier.
The current .c is enough for the function bodies above.
If you export HTML for BAS (and RTM if the caller of `CDBSENDCREATE` is there), drop it in `tbwp0007/` and I will walk the XREFs.
