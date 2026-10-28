# High-priority open items — status

> Superseded, 2026-10-16. Chapter 10. The disk-to-11 expansion row is not true. Read `TBdecompile/record/` for the claim. This sheet is the trail.

Date: 2026-10-14

## Page / background index

The `80 65` markers are a heap. Parent, z-order, and which background a page uses are not in the page record that has been decoded. TBX has Background.xml files (14 of them in the 9e954d01 export), so the relationship exists; it has not been mapped back to the binary.

**User can help:** In the TBX export, pick one page that uses a non-default background. Note the Background id. Then search the corresponding page record in the binary for that id (as a word or dword). If it appears, the index field is found. If it does not, the link is indirect (through a parent or a separate table).

## PaintPolygon type table

Static search closed. No on-disk bytes `76 03 08 14`. The table is built at runtime or fixed up by NE relocation. Registrar `FUN_1058_0a98` writes property id 0x4034, not painter pointers.

**User can help:** Once a book is open and a polygon page is painted:
- Break on the type dispatcher (BAS segment 0x7E / selector that was 3617 on a prior boot).
- Dump the table it indexes. The entry for PaintPolygon will be a far pointer with offset 0x376.
- Or break on PaintPolygon itself (BAS 0x82:0x376, selector moves) and walk one frame up. The return address is inside the dispatcher; the index is on the stack or in a register.

## Tbload vtable (ZZZTBKBOOKLOC)

`FUN_00405460` finds the marker. `FUN_00406a70` does a virtual call at `00406aa1` (vtable+4). That call is the first handoff out of the 32-bit search. The vtable has not been resolved in the listing.

**User can help:** Under a debugger on the 32-bit side (or SoftICE if Tbload is visible), break at `00406aa1`. The register or stack slot that holds the object pointer is the vtable base. Dump the first few entries. The slot at +4 is the function that receives the book location. That function is the next place to look for the signature check and the page-structure allocation.

## Property-block expansion

On disk: `14 00 00 01` + six words after the name. In memory (one SoftICE dump): `14 00 00 11`. Hypothesis: disk form is compacted; `CDBFILEOPEN` expands it and writes bounds at object+0xF. Not confirmed live.

**User can help:** Break on `CDBFILEOPEN` (BAS ordinal 8). When it returns, dump the object that was just created. Compare the six words after the name on disk with the same offset in the live object. If they differ, the expansion happened. If the live object has bounds at +0xF and the disk record does not, the write site is between the open call and the return.

## Summary — what needs a debugger

| Item | Break on | What to capture |
|------|----------|-----------------|
| PaintPolygon table | Type dispatcher or PaintPolygon | Table entry or return address + index |
| Tbload vtable | 00406aa1 | Object pointer, vtable+4 target |
| Property expansion | CDBFILEOPEN return | Live object vs disk record |
| Page/background index | (static first) | TBX background id in the binary page record |

The page/background index can be advanced without a debugger by using the TBX export as a map. The other three need a live break.
