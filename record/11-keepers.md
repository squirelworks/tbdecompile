# 11. Keepers

Addresses in this chapter are from the 2026-10-15 Windows 98 boots, DGROUP `347F`. Match a later boot on the `enter` size and the next two or three instructions, not on the selector. Decompile line numbers are from `TB80BAS.DLL.c` and do not move when the selector does.

`CDBSENDCREATE` is not in this list. It is author-only. See chapter 4.

## 11.1 File open and close

| Function | Live (one boot) | Enter | Decompile line | Role |
|---|---|---|---|---|
| `CDBFILEOPEN` | `4C7F:017A` | `000A` | 27592 | Book-open export. Ordinal 8. |
| `CDBFILECLOSE` | `4C7F:0948` | `0002` | 27965 | Close. Same caller cluster as open. |
| `CDBFILEPATH` | `4C7F:09E0` | `0002` | 28002 | Path query. |
| `CDBFILESTATUS` | `3ACF:0000` | `0004` | 30210 | Status. |
| `CDBQUERYMULTISAVE` | `4C7F:0B90` | `0018` | 28108 | Multi-save query. |
| `CDBMULTISAVE` | `4C7F:0E24` | `000C` | 28272 | Multi-save. |
| `OBJFILEOPEN` | `3147:177C` | `025A` | 76162 | Large frame. Buffered read. Downstream of the reader. |
| `OBJFILECLOSE` | `3147:10EA` | `0002` | 75887 | Object-file close. |
| `OBJGETFILE` | `3147:0094` | | | Object file access. Seen on the page path. |
| `OBJGETHDRLONG` | `3147:0242` | | | Header long. A 4-byte read here was an internal pointer, not a page header. |

`CDBFILEOPEN` callers seen: `322F:3252` (jump), `3D6F:0416` / `0F79` / `0E8E`, and the `3247` spine. `OBJFILEOPEN` callers include `3D6F`, `3247`, and `OBJGETFILE`.

## 11.2 Object lifetime

| Function | Live | Enter | Decompile line |
|---|---|---|---|
| `OBJFREE` | `3147:0CCC` | | 75619 |
| `OBJFREENEAR` | `3147:0D70` | | 75662 |
| `OBJUNLOCK` | | `004A` | call site, not a definition |
| `OBJREALLOCNEAR` | `3147:08D6` | `0018` | |
| `CDBCLEARBOOKREFS` | `4C7F:10A6` | `00B8` | 28451 |
| `CDBINIT` | | `00C8` | 30304 |

`HEAP*` / `TBHEAP*` hand out the `0x76`-byte object. `TBHEAPCLEARCRITSECT` was the last stop before a window appeared on one boot. `TBHEAPALLOC` and `TBHEAPFREE` are call sites throughout the decompile. There is no standalone `TBHEAPCLEARCRITSECT` definition in that listing.

## 11.3 Page, instance, and the value bus

These are closer to the unnamed reader than ordinal 51. On the 2026-10-15 captures, `CDBSENDCREATE` was listed in the Functions window and did not appear in the Calls stacks. `CDBCREATEPAGEREF` and `CDBSETVALUEEX` did.

| Function | Live | Enter | Decompile line | Note |
|---|---|---|---|---|
| `CDBCLASSTABLEGETBEHAVIOR` | `44F7:121A` | `0008` | 125154 | Splash gate. Unbreaking it let the splash run. |
| `CDBCREATEINSTANCE` | `480F:0000` | `0002` | 24974 | Instance constructor. |
| `CDBCREATEPAGEREF` | `483F:03B2` | | 25913 | Page reference. Next break. |
| `CDBVIEWNONE` | `483F:02F8` | `0002` | 25877 | View state. |
| `CDBVIEWPAGE` | | | 25726 | Ordinal 15. |
| `CDBVIEWBKGND` | | | 25825 | Ordinal 18. |
| `CDBSETVALUEEX` | `3397:147C` | | | Extended property set. Next break. |
| `CDBGETVALUE` | `3397:0D54` | | 38475 | Property bus. |
| `CDBGETVALUEEX` | | | 38488 | Extended get. |
| `CDBPARENTVALUE` | `3397:07B2` | | | Parent value. |
| `CDBDEREFVALUE` | `3397:0400` | | | Deref. |
| `CDBLOCKVALUE` | `3397:02CA` | `0002` | 37826 | Shifts `0B[bp]`. Not a record parser. |
| `CDBCLIENTSTATUS` | `480F:04C6` | | | Client status. |
| `CDBREGISTERINSTWINDOW` | `480F:0522` | | | Instance window. |
| `CDBDISPLAYSTATE` | `4877:0000` | | | Display state. |
| `CDBSYNCSCREENS` | `4877:0276` | | | End of the author create path. Seeing it does not mean ordinal 51 fired. |
| `CDBSENDSELECT` | `44CF:009E` | | | Select. Not create. |

Value constructors in segment `4267` fire often and are not the stream walker:

| Function | Live | Enter |
|---|---|---|
| `CDBVALUENEWBOOKREF` | `4267:0000` | `0004` |
| `CDBVALUEBOOKFROMSTRING` | `4267:03F4` | `0018` |
| `CDBVALUELAYERFROMSTRBOOK` | `4267:05F8` | `004C` |
| `CDBVALUERESOURCEFROMSTRING` | `4267:08B2` | `004A` |
| `CDBVALUEGRAPHICFROMSTRING` | `4267:0AA0` | `0074` |
| `VALUENEWBOOK` | `4267:0D90` | `0006` |
| `VALUENEWRESOURCE` | `4267:0EFC` | `000E` |
| `VALUENEWGRAPHIC` | `4267:1494` | `0008` |
| `CDBVALUENEWGRAPHICREF` | `4267:02D4` | |
| `CDBVALUENEWLAYERREF` | `4267:00C2` | |

`VALUENEWLONG` builds a long. It is not a record parser.

## 11.4 Chunk walkers

These walk characters: comma, CR, LF, tab, space, quote. A decompile that shows `ISDBCSLEADBYTE` and a comma test is this family.

| Function | Live | Enter | Decompile line | Callers |
|---|---|---|---|---|
| `CDBCHUNKEND` | `0D37:0000` | `0004` | 138456 | `3187:0210`, self from FIND |
| `CDBCHUNKFIND` | `0D37:0146` | `0008` | 138575 | `4857:0C68`, `3187:0210`, `322F:0577` |
| `CDBCHUNKLAST` | `0D37:0334` | `0010` | 138676 | `4857:090B`, `3187:0210` |

## 11.5 Paint and resource binding

| Function | Live | Decompile line | Note |
|---|---|---|---|
| `CDBPAINTCLIENT` | `389F:0506` | 13056 | Ordinal 26. RTM `WM_PAINT` ends here. |
| `IMBITBLT` | | 13277 | BitBlt path. |
| `IMDRAWLEVELS` | | 13353 | Draw levels. `IMDRAW` as a bare name is not a definition. |
| `IMBLACKOUTBMP` | | 13995 | |
| `IMINVERTBMP` | | 14021 | |
| `IMSHOWBMP` | | 14047 | |
| `RESMGREXTRACT` | | 21513 | Resource manager. |
| `RESMGREXTRACTGDI` | `4D27:1730` | 21523 | Extract for GDI. |
| `GETDIBCOLORCOUNT` | `35D7:053A` | | Enter `0006`. |
| `GETDIBSIZE` | `35D7:05DA` | not in the BAS or BMP listing | Enter `0008`. |
| `HUGEGETDATA` | `33BF:0D6C` | | Enter `0018`. Large fetch. |
| `COLORHLSTORGB` | `44B7:0B84` | 155991 | Menu color. Enter `0034`. Not the page painter. |

Painter offsets that do not move inside the segment are in chapter 8. `PaintPolygon` is BAS segment `0x82` offset `0x376`.

## 11.6 Incidental on open

Seen, and not the reader: `CDBREGISTEROLE2WINDOW` (`3767:0000`), `CDBREGISTERVBXFORM` (`4437:0000`), `VBXNEWVIEW` (`4437:0216`), `VALUEARRAYINFO` (`4357:02F2`), `VALUEARRAYSET` (`4357:0932`), `VALUEARRAYGET` (`4357:05D8`), `HEAPVALUETOPOINTER` (`450F:0F28`), `HEAPVALUETOFRAME` (`450F:0F4E`), `HEAPENTERCITSECT` (`450F:0DCE`), `HEAPLEAVECRITSECT` (`450F:0DF6`).

`?SENDPROC@TBXBOBJ@@` was seen at `29AF:0000` (`cmp ax, 3014`). The decompile does not contain `SENDPROC@TBXBOBJ` as that name. Related symbols are `_SETPROC_TBXBOBJ` at line 2175, `_SENDPROC_TBXLAYER`, `_SENDPROC_TBXBASE`, and `_SENDPROC_TBXUSER`.
