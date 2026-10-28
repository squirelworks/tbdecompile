# RTM-3 triage

> Trail, 2026-10-16. Chapter 17. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Counts

| Category | Count |
|----------|-------|
| Function definitions | 15,337 |
| Unique FUN_ names | 19,256 |
| Thunks | 612 |
| Ordinal_ calls | 15,186 (229 unique) |
| RECTANGLE calls | 18 |
| BITBLT calls | 77 |
| POLYGON calls | 0 |
| POLYLINE calls | 0 |
| CDB* calls | 37 (4 unique: CDBGETVALUEEX, CDBSAVEBOOK, CDBSENDVALUEEX, CDBSETVALUEEX) |
| File I/O (CREATEFILE/READFILE/etc) | 0 |

## Triage priority

1. **RECTANGLE callers** (18) — paint path, chip bodies.
2. **BITBLT callers** (77) — blit path, picture placement.
3. **CDB* callers** (4 unique) — property bus.
4. **Thunks** (612) — skip, stubs.
5. **Rest** — UI, memory, dispatchers.

## Notes

POLYGON and POLYLINE are not in RTM. Shape drawing is in BAS. File I/O is not in RTM. The record reader is not in RTM.
