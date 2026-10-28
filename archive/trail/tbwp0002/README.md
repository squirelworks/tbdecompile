# Symbol maps for TB80BAS and TB80RTM

> Trail, 2026-10-16. Chapter 7. Maps are NE-segment:offset and are not loaded as modules. If this sheet and `TBdecompile/record/` disagree, the record wins.

Generated from the Ghidra decompiles. One MAP per module.

| file | entries | source |
|------|---------|--------|
| TB80BAS.map | 3799 | TB80BAS_noghidra.DLL.c |
| TB80RTM.map | 2669 | TB80RTM.EXE.c |

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

SoftICE does not load this MAP directly. Two options:

1. Break on the BAS ordinal and walk back (no symbols needed):
   ```
   EXP TB80BAS
   BPX TB80BAS.Ordinal_51
   ```
   Or search for the call bytes `9A 20 07 F8 18` and break there.

2. Convert the MAP to a SYM if you have a converter. The MAP is the
   input. SoftICE loads SYM with the module if the name matches.

## WDW

WDW does not load this MAP as Watcom debug info. Use it as a lookup:

1. In WDW, note the live selector for the NE segment.
2. Find the function in the MAP (`13D0:0822 FUN_13d0_0822`).
3. Set the breakpoint at `selector:0822`.

Or break on BAS ordinal 51 and read the return address. That lands
inside RTM at the caller.

## Limits

- Offsets are from the unpacked image. They match the decompile.
- No types, no locals, no line numbers. Names and addresses only.
- The segment index must be matched to the live selector by hand.
