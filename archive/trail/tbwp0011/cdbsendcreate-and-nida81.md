**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Deeper CDBSENDCREATE XREF + nida81 Handler Surface

> Trail, 2026-10-16. Superseded. Chapters 4 and 15. Author-only correction wins. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## CDBSENDCREATE (12c8:00bc) — internal calls

From the BAS HTML listing, the function body contains:

- CALL FUN_12c8_0d94
- CALLF EXTERNAL:TB80UTL::TOOLBOOKFATAL
- CALL FUN_12c8_0850          ← object create / bounds write entry
- CALL FUN_12c8_0a86
- CALLF Code2:CDBSETSCRIPTPROPERTY
- CALL CDBCHECKBOUNDDTL (multiple sites: 12c8:01ec, 021a, 0249, 0277)
- CALL FUN_12c8_0e08
- CALL FUN_12c8_0d40
- CALLF Code3:CDBSYNCSCREENS
- CALL FUN_12c8_0d94 (again)

No named external callers appear inside BAS. The function is reached via ordinal (or from RTM/Tbload) and then drives the create path.

The `14 00 00` record reader that supplies the bounds/type arguments remains upstream and is still unnamed.

## nida81.tbk handler surface

From `system_handlers.json`:

- 100 handlers total.
- Almost all are buttonClick:
  - 87 × "TO HANDLE buttonClick"
  - 13 × "To Handle ButtonClick"
- Typical bodies set `lastbook` / `nextpage` and do `go to page "P…" of book "nida81.tbk"` or return to a previous book/page.
- No complex script logic; these are navigation stubs for the shell pages (P20000–P22130 range).

System .sbk files (nc81base/recs/test/trnr, tb80anm/hyp/r) have zero extracted handlers in the same dump.

## Status

- CDBSENDCREATE's internal call graph is now listed from the HTML.
- nida81.tbk is a thin navigation shell; its handlers do not contain the object-creation or graphics logic.
- The record-to-object parser is still the open gap.
