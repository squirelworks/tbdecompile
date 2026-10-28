**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Previously undisassembled regions — triage

> Trail, 2026-10-16. Superseded. Chapter 4. Author-path readings superseded. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Source

`/workspace/attachments/TB80BAS.DLL-4.c`

## Coverage

- `FUN_10b0_*`: 4062 hits
- `FUN_12e8_*`: 2335 hits
- Previously undisassembled regions are now decompiled.

## Largest functions

| Function | Lines | Notes |
|----------|-------|-------|
| `FUN_10b0_0f8e` | 6091 | Fatal call + stub |
| `FUN_10b0_0c11` | 2281 | Stub + error handler |
| `FUN_10b0_09ca` | 1258 | Dispatcher wrapper |
| `FUN_10b0_00fe` | 302 | Dispatcher |
| `FUN_10b0_1327` | 468 | Not sampled |
| `FUN_10b0_1400` | 383 | Not sampled |

## Patterns checked

- GDI calls (`POLYGON`, `POLYLINE`, `RECTANGLE`, `ELLIPSE`, `ARC`, `BITBLT`, `DRAWTEXT`): none in `FUN_10b0_*` or `FUN_12e8_*`.
- Object creation (`CDBSENDCREATE`, `FUN_12c8_0850`): none.
- Property handling (`0x4004`, `0x4023`, `0x402e`, `0x4034`, `0x4050`): none.
- String handling (`LSTRLEN`, `LSTRCPY`, `LSTRCAT`): none.
- Memory allocation (`GLOBALALLOC`, `LOCALALLOC`, `OBJNEW`): none.
- Calls to known interesting functions (`FUN_1008_*`, `FUN_12c8_*`, `FUN_1408_*`): none.

## Assessment

The previously undisassembled regions are mostly dispatchers, stubs, and error handlers. No GDI, no object creation, no property handling, no string handling, no memory allocation. Not worth deep analysis for the record reader or paint path.

## Worth keeping

- `FUN_12e8_0000` (OLE clone) is real and was previously noted.
- The rest are noise.
