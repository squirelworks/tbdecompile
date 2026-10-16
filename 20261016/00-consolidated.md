# Consolidated findings — 2026-10-16

> The short correction. `record/` is the expansion. This file does not add a later finding.

The full statement is [record/](../record/00-how-to-read.md), including the printable PDF. This file is the short correction that volume expands.

Brings the recent corrections and traces into the operating picture. Older notes that treated `CDBSENDCREATE` as a runtime waypoint are superseded by the finding below.

## 1. CDBSENDCREATE is author-only

`CDBSENDCREATE` (BAS ordinal 51, segment 12c8 offset 0xbc) creates or rewrites objects from the Instructor UI. It is not on the runtime book-open path. The runtime reader walks the TBK, recognizes `14 00 00` records, and creates objects without calling it. `FUN_12c8_0ef8` (bounds write) is also downstream of the author path.

Prior notes that listed it as a step between file open and object creation are closed for runtime research. See `tbworkingpapers/tbwp0025/cdbsendcreate-is-author.md`.

## 2. WDW traces (tbwp0026)

Three traces, no record reader.

- **W16** (11 shots): platform detection, OLE init, 32-bit thunk setup. No book open.
- **UTL** (53 shots): post-INITTASK utilities, task collections, help, metrics. No record walk.
- **BAS** (173 shots): value constructors (`VALUENEWLONG` is a constructor), `OBJFILEOPEN`, stack, chunk walkers. `CDBCHUNK*` are text walkers, not the page-record reader. `OBJFILEOPEN` is downstream of the reader.

The record reader is still in unstepped BAS. Next break is after `CDBFILEOPEN`.

## 3. Password cipher location

TBCBT NE segment 7 (Ghidra Code7:1030) holds `KEYEDPASSWORDENCRYPTEX`, `MAKEKEYEDPASSWORDEX`, `ENCRYPTEX`, and `DECRYPTEX`. It was not loaded in the SoftICE session that listed segments 01/0E/02/0B/08/0D/04/03. The dialog itself is a standard Windows dialog; the cipher is in segment 7.

After a failed password, the typed string and the constants `0xa01`/`0x300` remain in memory. Searching for them locates the call site even when segment 7 is unloaded.

## 4. File-open path status

SoftICE and WDW both reached `OBJFILEOPEN` and the buffered read in `FUN_1160_03de`. The raw DOS path at 04F3 is skipped when the buffer is satisfied. Dumps showed length 4 and an internal pointer, not a page header. The reader that turns the stream into `14 00 00` records is still unnamed.

## Open

- Runtime record reader (post-`CDBFILEOPEN`, pre-paint).
- Curve/arc/picture placement beyond bounds-only rectangles and kind=0400 polygons.
- Author-side binaries for a full Instructor path.
