# Full-file live session (append-style Save)

Filed 2026-10-17 from the Denny Dedmore exchange.

## Model

Ordinary Save appends. The engine loads the whole file, reapplies the append log, then presents the book. Only Save As writes a compact file.

Both `openscript_analysis` and `Foolbook` now load through a `LiveSession`:

- The session owns the ScriptHeap, ObjectArray, ObjectLayer, and ValueStack.
- `process()` walks the already-scanned pages and materializes page and field objects onto the live array.
- Trailing bytes after the last page are recorded as an `AppendRegion` (not yet interpreted).
- `view()` returns a finished Book only after `process()` has completed.
- The working live copy is not exposed to the viewer.

Public `load()` still returns a Book. The intermediate state is private.

## Files

- `openscript_analysis/tbk/openscript_analysis/live.py`
- `openscript_analysis/tbk/openscript_analysis/loader.py` (`_load_tbk`)
- `Foolbook/engine/live.py`
- `Foolbook/engine/loader.py` (`_load_tbk`)

## Open

The append-log format itself is not decoded. The session records the trailing region so a later pass can apply it. Until then, the live objects are the ones the full walk materialized.
