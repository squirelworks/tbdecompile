# WDW function tracing

> Trail, 2026-10-16. Chapter 12. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-16

## Capability

WDW has no full automatic call trace (no SoftICE-style `BPX ... DO` or WinDbg `wt`). You can log and continue on specific functions.

## Commands

| Command | Effect |
|---------|--------|
| `log <file>` | Redirect Log/Dialog output to file |
| `log >> <file>` | Append |
| `log` | Stop logging |
| `break <symbol> resume on` | Breakpoint fires, logs status, continues |
| `break <symbol> do <cmd>` | Action on hit |
| `hook <event> <cmd>` | Command on event (window-related) |

## Example

```
log c:\tbk\trace.log
break OBJFILEOPEN resume on
break CDBCHUNKFIND resume on
break CDBCHUNKLAST resume on
```

Run the book open. After the session, `log` to close. Each hit writes a status line.

## Limits

- You name the symbols. No "trace all calls."
- Live selectors change. Prefer export names if WDW resolves them.
- Log captures the status message, not registers or memory. Use a stop or a `do` that prints for that.
- Hook events are window-related, not call entry.

## SoftICE comparison

SoftICE: `BPX TB80BAS!OBJFILEOPEN DO "D SS:BP+6 L 10; P"`

WDW: `break OBJFILEOPEN resume on` plus external log file. Same idea, more setup.
