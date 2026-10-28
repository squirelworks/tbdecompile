# CDBSENDCREATE is an author function

> Trail, 2026-10-16. Chapter 4. The correction. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-15  
**Status:** Closed for runtime research

## Finding

`CDBSENDCREATE` (BAS ordinal 51, segment 12c8 offset 0xbc) is an author-side function. It is used when creating or editing objects in Instructor. It is not on the runtime book-open path.

## Why

The runtime reader walks the TBK, recognizes `14 00 00` records, and creates objects. That path does not call `CDBSENDCREATE`. The function is only reached when the authoring UI creates a new object or when an edit operation rewrites one.

## Impact

- Stop treating `CDBSENDCREATE` as a waypoint on the runtime record-reader path.
- Stop looking for callers of `CDBSENDCREATE` inside the book-open sequence.
- The record reader is still in BAS, but it is not the function that calls `CDBSENDCREATE`.
- `FUN_12c8_0ef8` (bounds write) is also downstream of the author path and is not the runtime record reader.

## Prior notes

The following notes treated `CDBSENDCREATE` as part of the runtime path. They are superseded by this finding:

- `tbwp0002/bas-create-path.md`
- `tbwp0008/cdbsendcreate-sites.md`
- Any note that lists `CDBSENDCREATE` as a step between file open and object creation for a loaded book.

## Next

The runtime record reader remains unnamed. It is either in an undisassembled BAS region or reached through a runtime-filled vtable. Live tracing of the book-open path (after `CDBFILEOPEN`, before the first object is painted) is still the way to find it. Do not break on `CDBSENDCREATE` for that purpose.
