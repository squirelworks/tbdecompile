# RTM nameable functions

> Trail, 2026-10-16. Chapter 8. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Thin wrappers

Functions that call exactly one API and return:

### Paint
- `FUN_1070_0be0`, `FUN_1098_14fc`, `FUN_1120_06da` — `BEGINPAINT`
- `FUN_1070_0be0`, `FUN_1120_06da` — `ENDPAINT`

### Window
- `FUN_1050_08aa`, `FUN_10a8_0062`, `FUN_10a8_1c3c` — `CREATEWINDOW`
- `FUN_1050_1566`, `FUN_1050_196a` — `DESTROYWINDOW`
- `FUN_1098_1b88`, `FUN_10d0_3166`, `FUN_1188_25ac` — `SHOWWINDOW`
- `FUN_10b8_33f0`, `FUN_1188_25ac`, `FUN_1188_267a` — `ENABLEWINDOW`
- `FUN_1060_0b80`, `FUN_1098_1ca0`, `FUN_10b8_33f0` — `SETFOCUS`
- `FUN_1060_0a48`, `FUN_1060_0b80`, `FUN_1098_0d44` — `GETFOCUS`
- `FUN_1010_0376`, `FUN_1070_063a`, `FUN_1070_07fa` — `INVALIDATERECT`

### Dialog
- `FUN_1188_2450`, `FUN_1188_2b8e` — `ENDDIALOG`

## API counts (not thin wrappers)

| API | Hits |
|-----|------|
| GETDLGITEM | 446 |
| SENDMESSAGE | 321 |
| LSTRLEN | 282 |
| GLOBALUNLOCK | 275 |
| GETWINDOWLONG | 275 |
| GLOBALLOCK | 210 |
| GLOBALFREE | 205 |
| LSTRCPY | 172 |
| ENABLEWINDOW | 131 |
| ISWINDOW | 79 |
| SETFOCUS | 63 |
| SHOWWINDOW | 56 |
| GETPARENT | 45 |
| INVALIDATERECT | 44 |
| SETWINDOWLONG | 39 |
| ENDDIALOG | 38 |
| GETFOCUS | 31 |
| POSTMESSAGE | 31 |
| DESTROYWINDOW | 28 |
| LOADCURSOR | 23 |
| SETWINDOWTEXT | 19 |
| PEEKMESSAGE | 19 |
| CREATEWINDOW | 17 |
| LOADBITMAP | 7 |
| DISPATCHMESSAGE | 7 |
| ENDPAINT | 7 |
| SETPARENT | 6 |
| TRANSLATEMESSAGE | 6 |
| BEGINPAINT | 5 |
| GETWINDOWTEXT | 4 |
| UPDATERECT | 3 |
| LOADICON | 2 |
| DIALOGBOX | 2 |
| GETMESSAGE | 2 |

## Not the record reader

These are UI and window management. The file open and the 14 00 00 reader are not among them.
