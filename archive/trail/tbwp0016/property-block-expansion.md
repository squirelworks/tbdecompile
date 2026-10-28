**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Property-block expansion

> Trail, 2026-10-16. Superseded. Chapter 4. FUN_12c8_0ef8 is author-side. The 01-to-11 mutation is not true. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## On disk

A typical widget record inside a page begins `14 00 00` followed by a subtype byte.
Example from P430 at page+0x9cb (a polygon):

```
14 00 00 00 c0 c0 c0 00 01 00 00 04 00 ...
```

The four words at source offsets `+0x3e / +0x40 / +0x42 / +0x44` in this record are point data, not the fields consumed by the create path.

## In the decompile

`FUN_12c8_0ef8` (called from `FUN_12c8_0e32` from `FUN_12c8_0850` from `CDBSENDCREATE`) reads four words from its source structure at exactly those offsets and writes them to the object at `+0x17 / +0x19 / +0x1b / +0x1d`.

The source structure that `FUN_12c8_0ef8` sees is not the raw `14 00 00` record. An earlier step (still unnamed) must expand or re-layout the disk record into the form the create path expects.

## Status

The field-copy site is known. The disk-to-source expansion that precedes it is not. A live break on `CDBFILEOPEN` (BAS ordinal 8) that dumps both the disk record and the structure passed to `FUN_12c8_0ef8` would show the expansion.
