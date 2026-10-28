# Record reader candidates

> Trail, 2026-10-16. Kept. Chapter 4.4. Candidates closed. If this file and `TBdecompile/record/` disagree, the record wins.

**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. It is not on the runtime book-open path. See `tbwp0025/cdbsendcreate-is-author.md`. Do not break on it for the runtime record reader.

Date: 2026-10-14

## Search results

| Pattern | RTM-3 | BAS-4 |
|---------|-------|-------|
| CDBSENDCREATE | 0 | 1 (definition only) |
| CDBNEWOBJECT | 0 | — |
| 0x14 comparison | — | several (type dispatch) |
| 14 00 00 literal | 0 | 0 |
| File I/O | 0 | — |

## Findings

- **CDBSENDCREATE** is defined in BAS. It is an author-side function, not part of the runtime book-open path.
- **FUN_10b0_00a6** (BAS) dispatches on type codes including 0x14. This is a type dispatcher, not a record reader.
- No function in RTM or BAS reads a far pointer and compares the first word to 0x14.
- The record reader is not in the decompiled regions.

## Next

- Do not break on CDBSENDCREATE for the runtime path.
- Force disassembly on remaining ?? runs in BAS that start with ENTER.
- The reader is still in BAS, but it does not call CDBSENDCREATE. Live tracing after CDBFILEOPEN is the remaining path.
