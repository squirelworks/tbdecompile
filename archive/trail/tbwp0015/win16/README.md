# win16

> Trail, 2026-10-16. Chapter 17. Win16 support notes for the unpacker. If this sheet and `TBdecompile/record/` disagree, the record wins.

Ghidra helpers for 16-bit NE binaries that Ghidra's auto-analysis leaves largely undefined.

## Scripts

- `ForceDisassembleC8.java` — force disassembly on every undefined `C8` (ENTER) byte
- `ForceDisassemblePrologues.java` — force disassembly on classic prologues (`55 8B EC`), Win16 export prologues (`45 55 8B EC 1E 8E D8`), the byte after RET/RETF, and NE entry-table addresses

Run C8 first, then Prologues. Both print a count of functions created.

## Notes

These recover functions that the NE loader and auto-analysis never flow into. They do not name anything. Naming still needs FIDB or manual work.
