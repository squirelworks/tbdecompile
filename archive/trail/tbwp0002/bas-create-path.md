# TB80BAS create path and object layout

> Trail, 2026-10-16. Superseded. Chapter 4. CDBSENDCREATE is not the runtime reader. If this file and `TBdecompile/record/` disagree, the record wins.

**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. It is not on the runtime book-open path. See `tbwp0025/cdbsendcreate-is-author.md`. The chain below is the author-side create path only.

From the honest unpack loaded in the patched Ghidra 12.1.4
(ghidra-win16, built 2026-10-12). Decompile is
`TB80BAS_noghidra.DLL.c` (220,276 lines). The entry table is intact:
segments 128-196 resolve, and named exports such as `CDBSENDCREATE`,
`CDBNEWOBJECT`, and `CDBCHECKBOUNDDTL` are visible.

## Object layout

- Object size is **0x76** bytes. `CDBNEWOBJECT` indexes them as
  `param_6 * 0x76`.
- Bounds are four words at **object+0xf, +0x11, +0x13, +0x15**
  (left, top, right, bottom). `CDBNEWOBJECT` reads exactly those.
- Flags byte at object+0x1f. Bits set from the source structure at
  +0x0a, +0x0c, +0x0e.
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
Ghidra matching constants against
`s_CTbkSimpleOLEDispatch_CallMethod` at `1630:100f`.

| param_5 | path |
|---------|------|
| 0x1014, 0x1015 | `FUN_12c8_0850` — new object |
| 0x1021, 0x1022 | `FUN_12c8_0a86` |
| 0x3018–0x301b | bounds-checked with `CDBCHECKBOUNDDTL`, then `FUN_12c8_0e08` |
| 0x3022 | `FUN_12c8_0d40` |
| else | `Ordinal_115` |

Parameters: `param_3`/`param_4` are the bounds pair (clamped against
32000 and 0x8300). `param_6`/`param_7` are compared to the current
object id (`DAT_1630_0164`/`0166`). `param_9` is an error out-byte
(`*param_9 = 0x13` on mismatch).

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

`FUN_1058_0a98` at **1058:0a98** (decompile line 30176). Builds the
property-id list. First write of `0x4004` is at decompile line 30313.
Nine writes of `0x4004` in the function.

Ids written: `0x4004` (bounds), `0x4009`, `0x400d`, `0x4015` (idNumber),
`0x401a`, `0x401b`, `0x401c`, `0x4020`–`0x4022`, `0x4023` (script),
`0x4027`, `0x402b`, `0x4031`–`0x4033`, `0x4034` (vertices), `0x4035`.

## Still open

`CDBSENDCREATE` receives bounds as parameters. It does not parse a
`14 00 00` record. The record-to-bounds reader is a caller of
`CDBSENDCREATE`, either in BAS or in the book-open path in RTM/Tbload.

Next step in Ghidra: list XREFs on `CDBSENDCREATE`. The caller that
passes a pointer into a page blob is the reader.

## Files

- Honest unpack: `tbworkingpapers/tbwp0001/TB80BAS_noghidra.DLL`
  (1,163,488 bytes, self-loading flag clear, entry segment bytes
  132–196).
- Decompile: attachment `TB80BAS_noghidra.DLL.c`.
- Ghidra project: attachment `TB80BAS_noghidra.DLL.gzf`.
- Ghidra patch: `toolbookunpacker/_external/ghidra12.x_fix/`.

## FUN_1058_0a98 detail

`ENTER 0x13c,0x0`. One caller: `FUN_1058_2bd8` at `1058:2c01`.

The function is a chain of success-gated blocks, one per object type.
Each block:

1. `FUN_1058_048e` — clear the descriptor.
2. `FUN_1058_04f8(type, ...)` — set the type code.
3. Fill a property-id list starting at `local_6` (almost always
   beginning with `0x4004`).
4. Set `local_24` (object size or property-block size).
5. `FUN_1058_2ae4(...)` — register. On success, fall through to the
   next type. On failure, return false.

Type-to-`local_24` map:

| type | local_24 | notes |
|------|----------|-------|
| 0x08 | 0x28 | |
| 0x0c | 0x28 | |
| 0x0d | 0x2c | |
| 0x0e | 0x33 | |
| 0x0f | 0x34 | polygon-like (matches 0ef8 case 0x0f) |
| 0x10 | 0x34 | polygon-like |
| 0x11 | 0x3b | arc (matches SoftICE type 0x11) |
| 0x12 | 0x39 | |
| 0x13 | 0x36 | |
| 0x14 | 0x36 | |
| 0x15 | 0x57 | |
| 0x19 | 0x57 | |
| 0x0b | 0x30 | starts with 0x41a4, not 0x4004 |
| 0x27 | 0x3d | |
| 0x1a | 0x100 | largest |

Common property prefix (most types): `0x4004`, `0x416f`, `0x4170`,
`0x4171`, `0x4009`, `0x400d`, `0x4015`, `0x4059`, `0x401a`, `0x401b`.
Type `0x0b` starts with `0x41a4` then `0x4004`. Type `0x1a` has a
longer list that includes `0x41ed`, `0x41f3`, `0x41ef`, `0x41f0`,
`0x4205`, `0x41f1`, `0x41f4`, `0x41f2`, `0x425c`, `0x424a`, `0x424b`,
`0x41ee`, `0x41f5`, `0x4230`, `0x4231`, `0x425d`.

The string displays (`s_Empty_ResourceTable + 0xf`, `s_DIBDESC + 2`,
`s_GOBJRARE + 2`) are the same constant-vs-address collision as in
`CDBSENDCREATE`. The real values are the numbers.
