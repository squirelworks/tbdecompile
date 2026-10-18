# How to fix Ghidra output

> Started 2026-10-17. Repair notes for listings and decompiler output. A repair is a procedure. It is not a claim about when the function runs. If this folder and `TBdecompile/record/` disagree, the record wins.

Ghidra here is 12.3, build DEV, 2026-10-14 00:43 JST, Java 25.0.4.1. Menus and script APIs from an older build do not apply until they are checked against this one.

## Notes

| Note | What broke | What fixed it |
|---|---|---|
| [01-call-return-split.md](01-call-return-split.md) | A Watcom function split at its jumps. Calls that return were marked `CALL_RETURN`. The bytes after them became `??`. | Clear the overrides, delete the fragment functions, disassemble from the entry, create the function with an explicit body. `scripts/FixObjFileOpen.java` is that pass for `OBJFILEOPEN`. |

## Adding a note

The next file is `02-`, then `03-`. One failure, one procedure. Keep the script that compiled, under `scripts/`, and name the public class the same as the file. Do not record a menu path or a method that this build rejected.

What belongs here:

- A listing symptom, and the listing after the repair.
- The script that ran, including the API this build does not have.
- Which analyzer will cut the function again if auto-analysis is turned back on.

What does not belong here:

- A new reading of a function's purpose. That goes in `record/` when it is asked for.
- A script that did not compile. The console line is enough, inside the note that replaced it.
