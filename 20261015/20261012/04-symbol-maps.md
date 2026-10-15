# Symbol maps

Generated from the Ghidra decompiles. Source: `tbwp0003/`.

| File | Entries | Source |
|------|---------|--------|
| `TB80BAS.map` | 3799 | TB80BAS_noghidra.DLL.c |
| `TB80RTM.map` | 2669 | TB80RTM.EXE.c |

## Format

```
SSSS:OOOO name
```

`SSSS` is the NE segment index from the decompile (for example `13D0`).
`OOOO` is the offset inside that segment. This is not a live selector.
The selector changes every boot. Match the segment index to the live
selector in the debugger, then use the offset.

Named exports (`CDBSENDCREATE`, `Ordinal_51`, etc.) replace the
`FUN_` name when the decompile attached one. Everything else keeps
the Ghidra name.

## SoftICE

SoftICE does not load this MAP directly.

1. Break on the BAS ordinal and walk back (no symbols needed):
   ```
   EXP TB80BAS
   BPX TB80BAS.Ordinal_51
   ```
2. Or convert the MAP to a SYM if you have a converter.

**Do not use `BAS(82)` or similar.** That is not a SoftICE address.
Use `MAP TB80BAS`, read the selector for the segment, then
`BPX <selector>:offset`.

## WDW

WDW does not load this MAP as Watcom debug info. Use it as a lookup:

1. Note the live selector for the NE segment.
2. Find the function in the MAP.
3. Set the breakpoint at `selector:offset`.

Or break on BAS ordinal 51 and read the return address.

## Limits

- Offsets are from the unpacked image. They match the decompile.
- No types, no locals, no line numbers. Names and addresses only.
- The segment index must be matched to the live selector by hand.
