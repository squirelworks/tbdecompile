# Object create path and bounds

> Duplicate of `TBdecompile/trail/20261012/`. Do not edit this copy. The current statement is `record/`.

From the honest unpack (`tbwp0001/TB80BAS_noghidra.DLL`) loaded in Ghidra.
Source writeup: `tbwp0002/bas-create-path.md`.

## Object layout

- Object size is **0x76** bytes. `CDBNEWOBJECT` indexes them as `param_6 * 0x76`.
- Bounds are four words at **object+0xf, +0x11, +0x13, +0x15** (left, top, right, bottom).
- Flags byte at object+0x1f. Bits set from the source structure at +0x0a, +0x0c, +0x0e.
- Source-structure fields copied by `FUN_12c8_0ef8`:
  - source+0x3e / +0x40 / +0x42 / +0x44 → object+0x17 / +0x19 / +0x1b / +0x1d
  - source+0x06 → object byte at offset given by a type table
  - source+0x04 → pattern lock

## Create path

```
CDBSENDCREATE          (12c8:00bc, Ordinal_51)
  └─ FUN_12c8_0850     (12c8:0850)   one caller only
       └─ FUN_12c8_0e32 (12c8:0e32)  allocator
            └─ FUN_12c8_0ef8 (12c8:0ef8)  field copier / bounds writer
```

`FUN_12c8_0850` is not the record reader. It locks context, calls the
allocator, and tears the object down on error. `ENTER 0x4,0x0`.

## CDBSENDCREATE type dispatch

`param_5` is the type code. The string arithmetic in the decompile is
Ghidra matching constants against `s_CTbkSimpleOLEDispatch_CallMethod`.

| param_5 | path |
|---------|------|
| 0x1014, 0x1015 | `FUN_12c8_0850` — new object |
| 0x1021, 0x1022 | `FUN_12c8_0a86` |
| 0x3018–0x301b | bounds-checked with `CDBCHECKBOUNDDTL`, then `FUN_12c8_0e08` |
| 0x3022 | `FUN_12c8_0d40` |
| else | `Ordinal_115` |

Parameters: `param_3`/`param_4` are the bounds pair (clamped against
32000 and 0x8300). `param_6`/`param_7` are compared to the current
object id. `param_9` is an error out-byte.

## FUN_12c8_0ef8 bounds write

Two paths write the four bounds words:

1. When `param_2` is null, copy from globals set from `param_4`/`param_5`:

```c
object+0x0f = DAT_1630_01fe;  // param_4
object+0x11 = DAT_1630_0200;  // param_5
object+0x13 = DAT_1630_0202;  // param_4
object+0x15 = DAT_1630_0204;  // param_5
```

2. In the `switch(param_6)` default case, copy four words from
   `param_2` into the same offsets.

`param_6` is the object type:

| param_6 | path |
|---------|------|
| 0x0f, 0x10, 0x13, 0x14 | polygon-like; `OBJNEWNEAR(param_1 << 2)` for a point array |
| 0x11, 0x12 | break (arc/pie; 0x11 matched the SoftICE arc) |
| 0x24 | special; also copies four words from `param_2` |
| default | copies `param_2[0..3]` into object+0xf..+0x15 |

## Property table

`FUN_1058_0a98` at **1058:0a98**. Builds the property-id list.
First write of `0x4004` is at decompile line 30313.
Nine writes of `0x4004` in the function.

Ids written: `0x4004` (bounds), `0x4009`, `0x400d`, `0x4015` (idNumber),
`0x401a`, `0x401b`, `0x401c`, `0x4020`–`0x4022`, `0x4023` (script),
`0x4027`, `0x402b`, `0x4031`–`0x4033`, `0x4034` (vertices), `0x4035`.

## Still open

`CDBSENDCREATE` receives bounds as parameters. It does not parse a
`14 00 00` record. The record-to-bounds reader is a caller of
`CDBSENDCREATE`, either in BAS or in the book-open path in RTM/Tbload.

Next step: list XREFs on `CDBSENDCREATE`. The caller that passes a
pointer into a page blob is the reader.
