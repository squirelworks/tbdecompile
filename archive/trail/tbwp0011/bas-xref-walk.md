**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# BAS XREF Walk — CDBSENDCREATE and Paint Functions

> Trail, 2026-10-16. Superseded. Chapter 4. Cross-references that start at ordinal 51 are the author path. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: `/workspace/attachments/TB80BAS.DLL.html`

## CDBSENDCREATE (12c8:00bc, ordinal 51)

- Function header XREFs are almost entirely internal locals (local_4 through local_26).
- One external-style note: `XREF[1]: Entry Point(*)`.
- No direct `CALL` / `CALLF` sites to the function start appear in the listing under the name; callers are expected to be in the book-open path (Tbload / RTM) or via ordinal import, not via a named near call inside BAS.
- Outgoing (from prior Ghidra listing): `FUN_12c8_0850`, `FUN_12c8_0e32`, `FUN_12c8_0ef8`, `CDBCHECKBOUNDDTL`, `CDBSYNCSCREENS`, `TOOLBOOKFATAL`, plus helpers.

The `14 00 00` record reader remains upstream of this entry.

## CDBSCALETWIPSTOSCREEN (1008:01dd)

21 XREFs (call sites). Sample:

- 1010:1c44, 1010:1ce6, 1010:1d8c, 1010:31b5, 1010:3a2d, 1010:3a75
- 1018:055f, 1018:05e3, 1018:0c21, 1018:0cea, 1018:1a24, 1018:1aa3
- 1020:09c6, 1020:1a28, 1020:1b02, 1020:1b10
- 10d8:0924, 10d8:0a24
- 1268:015f, 12d8:0cdc, 1500:0011

These are the known twip-to-screen scaling calls used by the painters.

## CDBPAINTPOLYGON (1408:0376)

- Local XREFs only in the header (local_4).
- Matches the known single painter in segment 0x82.
- Callers are via the type dispatcher (segment 0x7E) rather than a direct named call in the listing.

## CDBPAINTARC / CDBPAINTRECTANGLE

- Appear as near calls inside the 1020 segment (e.g. 1020:051b CALLF to CDBPAINTARC, 1020:01c6 CALL to CDBPAINTRECTANGLE).
- Cross-calls between the two are present.

## Summary

The HTML listing confirms the known entry points and shows that ScaleTwipsToScreen is widely called from the paint paths. CDBSENDCREATE has no internal named callers in BAS; its callers sit in the book-load path outside this DLL or via ordinal. The record parser that feeds it is still not named in the XREF data.

Next possible cut: dump the full 21 ScaleTwips call sites with surrounding context, or walk the type dispatcher that reaches PaintPolygon.
