# OpenScript expression path

> Trail, 2026-10-16. Chapters 6 and 14. FUN_1008_2d31. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Location

`FUN_1008_2d31` in TB80BAS segment 1008 is the expression evaluator.
It is reached from the 148-case switch at `1008:2dc7`.
The function checks for the string `"log"`, issues `FLD` / `FSTP` / `FCLEX`, and stays inside segment 1008.

This is the path for arithmetic and transcendental expressions in OpenScript.
It is not the page-record reader and not the widget-bounds writer.

## Engine status

`openscript_analysis` `1.0.0r5` records this location in `documentation/expression-evaluator.md`.
The engine (`core/engine.py`) still treats the right-hand side of an assignment as an opaque string.

## Next cut

A small evaluator that covers the operators already visible in the 1008 switch (`+`, `-`, `*`, `/`, and the named functions that reach `FUN_1008_2d31`) can be added beside the current engine without changing the decoder.
