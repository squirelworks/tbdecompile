# Object create path and bounds

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
            └─ FUN_12c8_0ef8 (12c8:0ef8)  writes bounds
```

`CDBSENDCREATE` does not parse a `14 00 00` record. It receives already-decoded bounds as parameters. The disk reader is a caller of `CDBSENDCREATE`, still unnamed.

## Type registrar

`FUN_1058_0a98` (1058:0a98) registers 15 types. Local_24 runs from 0x28 to 0x100. Type 0x11 (arc) is 0x3b. It writes property id 0x4034, not painter pointers.
