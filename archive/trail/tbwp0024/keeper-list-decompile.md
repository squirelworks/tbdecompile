# Keeper List — Decompile Locations

> Trail, 2026-10-16. Chapter 11. Line numbers in TB80BAS.DLL.c. If this sheet and `TBdecompile/record/` disagree, the record wins.

Line numbers from `TB80BAS.DLL.c`.

### File open / close
| Function | Line |
|----------|------|
| CDBFILEOPEN | 27592 |
| CDBFILECLOSE | 27965 |
| CDBFILEPATH | 28002 |
| CDBFILESTATUS | 30210 |
| CDBQUERYMULTISAVE | 28108 |
| CDBMULTISAVE | 28272 |
| OBJFILEOPEN | 76162 |
| OBJFILECLOSE | 75887 |

### Object lifetime
| Function | Line |
|----------|------|
| OBJFREE | 75619 |
| OBJFREENEAR | 75662 |
| CDBCLEARBOOKREFS | 28451 |
| CDBINIT | 30304 |

OBJUNLOCK is a call site, not a definition in the decompile.

### Chunk / record
| Function | Line |
|----------|------|
| CDBCHUNKFIND | 138575 |
| CDBCHUNKEND | 138456 |
| CDBCHUNKLAST | 138676 |
| CDBLOCKVALUE | 37826 |

### Resource / graphics binding
| Function | Line |
|----------|------|
| RESMGREXTRACTGDI | 21523 |
| RESMGREXTRACT | 21513 |
| VALUENEWRESOURCE | 90660 |
| COLORHLSTORGB | 155991 |

GETDIBSIZE: not found in BAS or BMP decompiles.

### Paint path
| Function | Line |
|----------|------|
| CDBPAINTCLIENT | 13056 |
| IMBITBLT | 13277 |
| IMDRAWLEVELS | 13353 |
| IMBLACKOUTBMP | 13995 |
| IMINVERTBMP | 14021 |
| IMSHOWBMP | 14047 |

IMDRAW as a standalone name: not found (IMDRAWLEVELS is the entry).

### Property / value bus
| Function | Line |
|----------|------|
| CDBGETVALUE | 38475 |
| CDBGETVALUEEX | 38488 |

### Instance / class
| Function | Line |
|----------|------|
| CDBCLASSTABLEGETBEHAVIOR | 125154 |
| CDBCREATEINSTANCE | 24974 |
| CDBVIEWNONE | 25877 |
| CDBCREATEPAGEREF | 25913 |
| CDBVIEWPAGE | 25726 |
| CDBVIEWBKGND | 25825 |

### Heap
TBHEAPALLOC / TBHEAPFREE are call sites throughout. No standalone TBHEAPCLEARCRITSECT definition found in the decompile.

### Supporting
SENDPROC@TBXBOBJ: not found. Related: `_SETPROC_TBXBOBJ__TCJPAEPEV1_GJJ_Z` at line 2175, `_SENDPROC_TBXLAYER`, `_SENDPROC_TBXBASE`, `_SENDPROC_TBXUSER`.
