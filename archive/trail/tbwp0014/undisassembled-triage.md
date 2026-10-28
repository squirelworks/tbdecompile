**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Triage of the 165 ?? runs

> Trail, 2026-10-16. Superseded. Chapter 4. Author-path readings superseded. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Ranking

| Score | Count | Meaning |
|-------|-------|---------|
| 3 | 108 | Starts with `C8` (ENTER) or `90 C8` (NOP + ENTER). Real functions. |
| 2 | 3 | Starts with a far call/jmp or XOR/SUB AX,AX. Probably code. |
| 1 | 54 | Other. May be data, jump tables, or code with an unusual prologue. |

The 108 score-3 runs are the ones worth forcing disassembly on. The largest:

| Lines | Address | First bytes |
|-------|---------|-------------|
| 5167 | 10b0:1e23 | 90 C8 6A 00 00 56 2B C0 |
| 3528 | 12e8:0000 | C8 CA 00 00 57 56 C6 46 |
| 3043 | 12e8:1a77 | 90 C8 32 00 00 C7 46 E6 |
| 2786 | (13f0) | C8 9C 00 00 56 2B C0 89 |
| 2428 | 10b0:0000 | C8 70 00 00 2B C0 89 46 |
| 2254 | 1278:5de4 | C8 CC 00 00 57 56 FF 76 |
| 2110 | (1540) | C8 26 00 00 56 C4 5E 0C |
| 2053 | (13f0) | 90 C8 A8 00 00 57 56 C4 |

Code94 (12e8:0000) is the second-largest and has already been decompiled: it is OLE object clone/copy, not the book path.

## How to force them

In Ghidra, for each score-3 address:

1. Go to the address.
2. Select the run (or just the first byte).
3. Press D (Disassemble).
4. If a function is not created, press F (Create Function).

A script can do the same: find undefined `C8` bytes, call `disassemble`, then `createFunction`.

## What to look for after disassembly

Once a run is turned into functions, search the decompile for:

- `14 00 00` or a word compare against 0x14
- Calls to `CDBSENDCREATE`, `CDBNEWOBJECT`, or `FUN_12c8_0850`
- String references to "page", "background", "bounds", "vertices"
- Loops that walk a buffer and write to object+0xF

Most of the 108 will be ordinary support code (OLE, memory, string, GDI helpers). The record reader, if it is in one of these runs, will stand out by those patterns.

## Status

108 runs are real functions waiting for a Disassemble. The rest are lower priority. Code94 has been checked and is OLE support.
