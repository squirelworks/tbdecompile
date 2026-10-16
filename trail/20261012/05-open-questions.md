# Open questions

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

## Bounds

- Disk `14 00 00` record → object+0xF expansion rule. Caller of `CDBSENDCREATE` still unnamed.
- Property-block expansion: `FUN_12c8_0ef8` copies source+0x3e/+0x40/+0x42/+0x44. Disk layout does not match those offsets.

## Graphics

- Curve control structure (P420). Points exist; order/header unknown.
- Arc disk layout. Live object type 0x11 known; no matching disk pattern.
- Picture id → DIB. 641 BMPs carved. Widget field not identified.
- Computed shapes (brackets) built from bounds in segment 0x5B.

## Runtime

- RTM book-open path. Unicorn host dies before any DOS open.
- CMP W16 segment-not-present fault on expand.
- PaintPolygon type table is runtime-built. No static pointer.

## OpenScript

- Full expression evaluator. Current engine covers arithmetic and a few functions.
- System-book contract for .fsk.

## Authoring

- CMP expand. W16 fault blocks a compile+expand test.
- Instructor 11.5 Save To XML path (Denny notes).
