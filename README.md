# TBDecompile

ToolBook 8.1 decompilation notes, segment maps, and research documentation.

## Contents

- `20261012/` — consolidated notes from the 12 October 2026 session
  - Object create path, graphics painters, OpenScript, symbol maps, open questions, debugger notes
  - BAS/RTM/W16 export maps and ordinal map
- `maps/` — NE segment to Ghidra space mappings
- `rename/` — Ghidra rename scripts index and naming progress
- `research/` — key analysis notes (CDBSENDCREATE, property expansion, RTM paint path, closed candidates)

## Status

Record reader still unnamed. `CDBSENDCREATE` (BAS ordinal 51, 12c8:00bc) receives bounds as parameters; it does not parse `14 00 00`. The disk reader is a caller of `CDBSENDCREATE`, still not located.

Live SoftICE confirmation of the create path is pending. Curve and arc disk layouts remain open.

Full local trees (MAP files, complete rename scripts, TB80BAS.map / TB80RTM.map) stay in the working papers.
