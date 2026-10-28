# Medium-priority open items — status

> Trail, 2026-10-16. Chapter 10. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Remaining draw-object layouts

| Object | Status | What is known | What is open |
|--------|--------|---------------|--------------|
| Polygon | Solved | kind=0400, count at +0x1A, points at +0x22, painter at BAS 1408:0376 | Per-pin position index (+0x52) not yet applied |
| Arc | Layout known | type 0x11, four twip pairs at +0x25, painter at BAS seg 0x7B | Angles not located; no on-disk match yet |
| Curve | Points found | P420 record +0xA13 has real screen points (~400-500) | Control structure unknown. Type ID 0x05C7 not in the page. Order/structure wrong when rendered |
| Picture | Partial | BMPs carved; TBX expands to Vertices | Resource ID to widget binding still open |

**User can help:** A SoftICE/WDW break on the curve painter (or on GDI!POLYLINE when a curve is drawn) will show whether the points are stored or computed. Same for arc angles.

## System-book scripts

Triage done (tbwp0007/sbk-triage.md). Core NIDA books are tb80r, nc81base/recs/test/trnr. They are resource containers (type tables, menus). Live handlers are in nc81int.dll / nc81rec.dll, already decompiled. No further static work needed for playback.

**User can help:** Nothing static. Runtime traces of `initializebase` / `initializerecs` calls will show what the lessons actually invoke.

## OpenScript token map

Decoder works for the common subset (goto, send, assign, if/else, step). High-byte back-references are fixed. Gaps remain on less common opcodes and on handlers that the current decoder drops at the first standalone `end`.

**User can help:** Compile one known handler in a real ToolBook instance and expand it with `COMPILEREXPANDTEXT`. That gives the ground-truth token map. Without that, the gaps stay.

## Picture-binding ids

BMPs are carved. TBX matches 67 markers to 72 bitmaps. The binding from a page widget to a specific BMP resource id is not fully decoded.

**User can help:** A break on `TBKGETGRAPHICID` or `TBKGRAPHICFX` (TB80W16) when a page with a known picture paints will show the id that is requested and the object it belongs to.

## Summary

| Item | Static progress | Needs user |
|------|-----------------|------------|
| Curve control structure | Points found, structure unknown | Live trace on curve painter |
| Arc angles | Layout known, angles missing | Live trace on arc painter |
| Picture binding | BMPs carved, ids not tied | Break on TBKGETGRAPHICID |
| OpenScript gaps | Common subset works | Compile+expand one handler |
| System books | Triage done, logic in DLLs | Runtime traces of init calls |

Moving to high-priority items next.
