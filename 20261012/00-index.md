# TBdecompile — Decompile Notes Index

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

Consolidated notes from the ToolBook II 8.1 reverse-engineering work.
Sources: BAS/RTM decompiles, SoftICE field notes, tbwp0002–0004, and the
NIDA system-book analysis.

## Contents

| File | Topic |
|------|-------|
| [01-object-create-path.md](01-object-create-path.md) | Object layout, CDBSENDCREATE, bounds writer |
| [02-graphics-painters.md](02-graphics-painters.md) | Polygon, rectangle, arc, scale, picture |
| [03-openscript-and-system.md](03-openscript-and-system.md) | Decoder, NIDA system books, tb80r compression |
| [04-symbol-maps.md](04-symbol-maps.md) | BAS/RTM maps and debugger usage |
| [05-open-questions.md](05-open-questions.md) | Remaining gaps |
| [06-debugger-notes.md](06-debugger-notes.md) | SoftICE/WDW cautions and correct breakpoint form |

## Key confirmed facts

- Object size is 0x76 bytes. Bounds are four words at object+0xF.
- `CDBSENDCREATE` receives bounds as parameters; it does not parse `14 00 00`.
- The bounds writer is `FUN_12c8_0ef8`. The disk reader is a caller of `CDBSENDCREATE`.
- Polygon painter: `FUN_1408_0376`. Scale: `FUN_1008_01dd` (stored/15 at DPI 96).
- OpenScript decoder handles the NIDA navigation patterns. tb80r uses the same bytecode.
- moralrecordings FIDBs produce no CRT renames. Compiler is Microsoft C (R60xx).

## Still open

- Disk `14 00 00` → object+0xF expansion rule (caller of `CDBSENDCREATE`).
- Curve control structure (P420).
- Arc disk layout match.
- Picture id → DIB binding.
- RTM book-open path (dies before open in Unicorn).
- CMP W16 segment-not-present fault.
