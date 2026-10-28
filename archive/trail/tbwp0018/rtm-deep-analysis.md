# RTM deep analysis

> Trail, 2026-10-16. Chapters 5 and 17. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## GETDLGITEM (446 hits)

Control ID counts (top):

| ID | Count |
|----|-------|
| 0x65 (101) | 55 |
| 0x67 (103) | 12 |
| 0xDB8 (3512) | 12 |
| 0x11E3 (4579) | 10 |
| 1 | 9 |
| 0xA2C (2604) | 9 |
| 0xA36 (2614) | 9 |
| 0x73 (115) | 9 |

ID 101 is the most common. In the first sample, it is used after `SETWINDOWTEXT` on a path string (`anxModifyPathSource`). The function loads three string IDs (`0x13b3`, `0x13b5`, `0x13b4`) and walks them.

Top callers: `FUN_1068_0000` (12), `FUN_1370_03da` (6), `FUN_13e0_0fe4` (5).

## SENDMESSAGE (321 hits)

Decompiler output is mangled. Most calls have truncated arguments. Known message IDs:

| ID | Count |
|----|-------|
| 0x111 | 2 |
| 0x113 | 1 |
| 0x118 | 1 |

Top callers: `FUN_1068_0000` (6), `FUN_10b8_2f4a` (3), `FUN_1068_0034` (3).

## LSTRLEN (282 hits)

Decompiler output is mangled. Top callers: `FUN_1020_1fbc` (9), `FUN_1008_02c4` (7), `FUN_1068_0000` (3).

## GLOBALLOCK (210) / GLOBALUNLOCK (275) / GLOBALFREE (205)

`FUN_1068_0098` is a `GLOBALALLOC` wrapper with retry. It calls `FUN_1068_00d0` which shows a dialog (`0xd`, `0x35`) and retries if the user chooses 4. This is an out-of-memory handler.

Top `GLOBALLOCK` caller: `FUN_1068_0098` (49). This is the allocator, not a locker. The lock/unlock/free counts are spread across many functions.

## GETWINDOWLONG (275 hits)

Index counts:

| Index | Count | Meaning |
|-------|-------|---------|
| 10 | 196 | custom offset |
| 8 | 35 | custom offset |
| 0xFFF0 (-16) | 30 | `GWL_WNDPROC` or similar |
| 26 | 4 | |
| 2 | 3 | |
| 0xFFFC (-4) | 2 | `GWL_WNDPROC` |
| 12 | 1 | |
| 16 | 1 | |
| 20 | 1 | |
| 0 | 1 | `GWL_USERDATA` |
| 0xFFFC | 1 | |

Index 10 is the most common. In the first sample (`FUN_10d0_3166`), it reads a pointer and checks `*piVar5 != 0`.

Top callers: `FUN_10d0_3166` (7), `FUN_10d0_0000` (4), `FUN_10b8_1588` (3).

## Named functions

| Function | Role |
|----------|------|
| `FUN_1068_0098` | `GLOBALALLOC` with retry on OOM |
| `FUN_1068_00d0` | OOM dialog, returns 4 to retry |
| `FUN_1068_0000` | dialog helper, top caller of `GETDLGITEM` and `SENDMESSAGE` |
| `FUN_10d0_3166` | window long reader, top caller of `GETWINDOWLONG` |

## Not the record reader

These are UI, dialog, and memory management. The file open and the 14 00 00 reader are not among them.
