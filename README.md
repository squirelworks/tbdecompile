# TBDecompile

ToolBook 8.1 decompilation notes, segment maps, and research documentation.

## Contents

- `20261012/` — the 12 October consolidation: create path, painters, OpenScript, symbol maps, debugger notes, export maps
- `20261014/` — the working papers, condensed. Findings, what is still open, the 11.5 export, and what the shelf was
- `maps/` — NE segment to Ghidra space
- `rename/` — Ghidra rename scripts and the nameable lists
- `research/` — the short notes that `20261014/` supersedes

## Status

The record reader is still unnamed. `CDBSENDCREATE` receives bounds as parameters and does not parse `14 00 00`. The disk reader is a caller of it, and it has not been found. Content rectangles and the polygon record are decoded. Curves, arcs, and picture placement are not.

Binary dumps stay out of this repository. Personal names stay out. The correspondent is JohnDoe1.
