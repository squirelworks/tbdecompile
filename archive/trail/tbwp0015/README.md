# ForceDisassemblePrologues

> Trail, 2026-10-16. Chapter 17. C8 pass, then prologue pass. If this sheet and `TBdecompile/record/` disagree, the record wins.

Companion to ForceDisassembleC8.java.

Walks undefined regions and forces disassembly + createFunction on:

- `55 8B EC` (classic PUSH BP / MOV BP,SP)
- `45 55 8B EC 1E 8E D8` (Win16 export prolog)
- the byte immediately after a `C3` or `CB` (RET / RETF)
- every NE entry-table address that has no function

Run from Script Manager after the C8 pass.
