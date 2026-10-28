# TB80BAS Keepers Ledger (WDW)

> Trail, 2026-10-16. Chapter 11. Enter sizes. Selectors are that boot. If this sheet and `TBdecompile/record/` disagree, the record wins.

Practical cut of functions that sit on the book-open, object-create, or render path. All functions are logged in wdw-to-ghidra.md. This file tracks only the keepers.

Addresses are for the 2026-10-15 boots (DGROUP 347F). Match on enter size + next instructions on later boots.

## Keepers

| Function | Address | Enter | Notes |
|----------|---------|-------|-------|
| CDBCLASSTABLEGETBEHAVIOR | 44F7:121A | 0008,00 | Splash-gate. Unbreaking let splash run. |
| CDBCREATEINSTANCE | 480F:0000 | 0002,00 | Instance constructor. |
| CDBVALUENEWBOOKREF | 4267:0000 | 0004,00 | Book-ref constructor. |
| CDBVALUEBOOKFROMSTRING | 4267:03F4 | 0018,00 | Book-from-string. Calls LSTRLEN. |
| CDBVALUEGRAPHICFROMSTRING | 4267:0AA0 | 0074,00 | Graphic-from-string. Large frame. |
| CDBVALUELAYERFROMSTRBOOK | 4267:05F8 | 004C,00 | Layer-from-string-book. |
| CDBVALUERESOURCEFROMSTRING | 4267:08B2 | 004A,00 | Resource-from-string. |
| VALUENEWGRAPHIC | 4267:1494 | 0008,00 | Graphic value. |
| VALUENEWBOOK | 4267:0D90 | 0006,00 | Book value. |
| GETDIBCOLORCOUNT | 35D7:053A | 0006,00 | DIB color count. Graphics. |
| HUGEGETDATA | 33BF:0D6C | 0018,00 | Large data fetch. |
| OBJREALLOCNEAR | 3147:08D6 | 0018,00 | Near realloc. Object lifetime. |

| GETDIBSIZE | 35D7:05DA | 0008,00 | DIB size. Graphics path. |
| VALUENEWRESOURCE | 4267:0EFC | 000E,00 | Resource value constructor. |

## Matching note

`mov ax,347F` is this boot's DGROUP. Match on enter size and the next 2-3 instructions.
