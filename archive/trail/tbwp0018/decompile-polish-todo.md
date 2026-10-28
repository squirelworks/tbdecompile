# Decompile polish todo

> Trail, 2026-10-16. Chapter 17. Polish is not the reader. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

Bookmark for when the decompile is polished.

## SENDMESSAGE (321 hits)

Decompiler output is mangled. Most calls have truncated arguments. Known message IDs:

| ID | Count |
|----|-------|
| 0x111 | 2 |
| 0x113 | 1 |
| 0x118 | 1 |

Top callers: `FUN_1068_0000` (6), `FUN_10b8_2f4a` (3), `FUN_1068_0034` (3).

The decompiler is not recovering the message ID argument. A re-decompile with better calling convention or manual annotation would recover the message IDs.

## LSTRLEN (282 hits)

Decompiler output is mangled. Top callers: `FUN_1020_1fbc` (9), `FUN_1008_02c4` (7), `FUN_1068_0000` (3).

The decompiler is not recovering the string pointer argument. A re-decompile with better calling convention or manual annotation would recover the strings.

## GETDLGITEM (446 hits)

Partially recovered. Control IDs are visible. Top ID is `0x65` (101, 55 hits). Top caller is `FUN_1068_0000` (12).

## GETWINDOWLONG (275 hits)

Partially recovered. Index values are visible. Top index is 10 (196 hits). Top caller is `FUN_10d0_3166` (7).

## Notes

These are not the record reader. They are UI and string helpers. Bookmark for a decompile polish pass.
