# TB80RTM triage

> Trail, 2026-10-16. Chapter 17. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Scale

163173 lines. 134 segments. ~9363 function references (inflated by repeated names). Top segments by reference count: 1008 (969), 1040 (512), 1068 (358), 10b8 (350), 1148 (289).

## Character

Windows UI and memory management heavy. Top named tokens: `GETDLGITEM` (446), `SENDMESSAGE` (321), `LSTRLEN` (282), `GLOBALUNLOCK` (275), `GETWINDOWLONG` (275), `GLOBALLOCK` (210), `GLOBALFREE` (205), `LSTRCPY` (172).

No `_lopen`, `_lread`, `OpenFile`, `ReadFile`, `CreateFile`, `JBO`, or `ZZZTBKBOOKLOC` in the decompile. File open is not visible as a named call.

## Named CDB functions

- `CDBSAVEBOOK` — save path. Checks `LSTRLEN` and DGROUP flags before proceeding.
- `CDBGETVALUEEX` — property getter. Calls with property id `0x4015` (`idNumber`).
- `CDBSENDVALUEEX`, `CDBSETVALUEEX` — property send/set.

These are the property bus, not the record reader.

## 14 00 00

485 hits on `0x14`. None are a stream walker that compares the first word of a far pointer to `0x0014`. Same situation as BAS.

## Next

The file open is not a named call in this decompile. It is either an un-named Windows API thunk, or it lives in a segment that Ghidra did not flow into. A live break on `CDBFILEOPEN` (BAS ordinal 8) and a walk up the stack is still the shortest path to the reader.
