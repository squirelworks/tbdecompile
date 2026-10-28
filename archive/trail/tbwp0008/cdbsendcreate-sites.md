# CDBSENDCREATE Call Sites — BAS

> Trail, 2026-10-16. Superseded. Chapter 4. Callers are author-side. If this file and `TBdecompile/record/` disagree, the record wins.

**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. It is not on the runtime book-open path. See `tbwp0025/cdbsendcreate-is-author.md`. Do not use this as a waypoint for the runtime record reader.

Date: 2026-10-14

## Summary

`CDBSENDCREATE` (BAS ordinal 51, segment 12c8 offset 0x00bc) is the entry that receives already-extracted bounds and type information and creates the runtime object. The on-disk `14 00 00` record reader is still upstream of this call.

Object size is 0x76 bytes. Bounds are written at object+0x0f / +0x11 / +0x13 / +0x15.

## Call chain (from earlier analysis)

```
CDBSENDCREATE (12c8:00bc)
  → FUN_12c8_0850
    → FUN_12c8_0e32
      → FUN_12c8_0ef8   (writes bounds, type dispatch)
```

Type dispatch in `FUN_12c8_0ef8` (param_6):

| param_6     | Path                                      |
|-------------|-------------------------------------------|
| 0x0f, 0x10, 0x13, 0x14 | polygon-like; allocates point array |
| 0x11, 0x12  | arc / pie (0x11 confirmed SoftICE)        |
| 0x24        | special                                   |
| default     | bounds copy only                          |

Property registrar is `FUN_1058_0a98` (1058:0a98). Type 0x11 (arc) gets local_24 = 0x3b.

## Outgoing references (from earlier Ghidra listing)

- FUN_12c8_0d94
- TOOLBOOKFATAL
- FUN_12c8_0850
- FUN_12c8_0a86
- FUN_1008_03f6
- CDBCHECKBOUNDDTL
- FUN_12c8_0e08
- FUN_12c8_0d40
- CDBSYNCSCREENS

## Still open

The caller that reads a `14 00 00` record from the page blob and passes the extracted bounds / type into `CDBSENDCREATE` has not been located. Next step is XREF walk on the ordinal or on the function start in the full BAS listing.

## Files

- HTML listing: `/workspace/attachments/TB80BAS.DLL.html` (and TB80BAS_noghidra.DLL.html)
- Prior notes: `tbworkingpapers/tbwp0002/bas-create-path.md`
