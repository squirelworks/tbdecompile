# Symbol maps

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

Generated from the Ghidra decompiles. Source: `tbwp0003/`.

| File | Entries |
|------|---------|
| TB80BAS.map | 3799 |
| TB80RTM.map | 2669 |

Format is NE-segment:offset name. Segment index is not a live selector.

SoftICE and WDW do not load the MAP directly. Use it as a lookup, or break on the ordinal.

- BAS ordinal 51 is `CDBSENDCREATE`.
- The NE-to-Ghidra space map is in `maps/rtm-ne-to-ghidra.md`.
