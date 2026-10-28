**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# Keeper List

> Trail, 2026-10-16. Kept. Chapter 11. Live addresses. CDBSENDCREATE removed. If this file and `TBdecompile/record/` disagree, the record wins.

Sorted by role. CDBSENDCREATE removed.

### File open / close
- **CDBFILEOPEN** (`4C7F:017A`) — book open entry. `enter 000A,00`. Callers: `322F:3252` (jmp), `3D6F:0416/0F79/0E8E`, `3247:*`.
- **CDBFILECLOSE** (`4C7F:0948`) — file close. `enter 0002,00`. Same caller cluster as OPEN.
- **CDBFILEPATH** (`4C7F:09E0`) — path query. `enter 0002,00`.
- **CDBFILESTATUS** (`3ACF:0000`) — file status. `enter 0004,00`. Callers: `3D6F:`, `3247:`.
- **CDBQUERYMULTISAVE** / **CDBMULTISAVE** (`4C7F:0B90` / `0E24`) — multi-save. `enter 0018` / `000C`.
- **OBJFILEOPEN** (`3147:177C`) — object file open. `enter 025A` (large). Callers: `3D6F:`, `3247:`, `OBJGETFILE`.
- **OBJFILECLOSE** (`3147:10EA`) — object file close. `enter 0002,00`.

### Object lifetime
- **OBJFREE** / **OBJFREENEAR** (`3147:0CCC` / `0D70`) — teardown.
- **OBJUNLOCK** (`enter 004A,00`) — unlock.
- **CDBCLEARBOOKREFS** (`enter 00B8,00`) — book ref cleanup.
- **CDBINIT** (`enter 00C8,00`) — large init.

### Chunk / record
- **CDBCHUNKFIND** (`0D37:0146`) — callers: `4857:0C68`, `3187:0210` (far), `322F:0577`. `enter 0008`, reads `12[bp]`.
- **CDBCHUNKEND** (`0D37:0000`) — callers: `3187:0210` (far), self from FIND. `enter 0004`, compares `0C[bp]`.
- **CDBCHUNKLAST** (`0D37:0334`) — callers: `4857:090B`, `3187:0210` (far). `enter 0010`, zeros locals.
- **CDBLOCKVALUE** (`3397:02CA`) — callers: `4857:0C68`, `3187:0210` (far), `31B7:0073`. `enter 0002`, shifts `0B[bp]`.

### Resource / graphics binding
- **RESMGREXTRACTGDI** (`4D27:1730`) — resource extract for GDI. `push bp / mov bp,sp`.
- **RESMGREXTRACT** — resource manager entry (bitmaps, patterns).
- **GETDIBSIZE** / **VALUENEWRESOURCE** — graphics size and resource constructor.
- **COLORHLSTORGB** (`44B7:0B84`) — HLS-to-RGB. `enter 0034,00`. Fires on menu draw. Supporting only.

### Paint path
- **CDBPAINTCLIENT** (`389F:0506`) — live paint entry.
- **IMDRAWLEVELS**, **IMBITBLT**, **IMBLACKOUTBMP**, **IMDRAW**, **IMSHOWBMP**, **IMINVERTBMP** — reach GDI (POLYGON, POLYLINE, RECTANGLE, BitBlt).

### Property / value bus
- **CDBGETVALUE** (`3397:0D54`) — property/value bus. `push bp / mov bp,sp`.
- **CDBGETVALUEEX** — extended property bus.

### Instance / class
- **CDBCLASSTABLEGETBEHAVIOR** (`44F7:121A`) — on the book-open path. Unbreaking it let the splash run.
- **CDBCREATEINSTANCE** (`480F:0000`) — instance constructor. Callers include value-from-string functions.
- **CDBVIEWNONE** (`483F:02F8`) — view state. `enter 0002,00`.
- **CDBCREATE*REF** (graphic, page, background) / **CDBVIEW*** — page/object construction.

### Heap
- **HEAP*** / **TBHEAP*** — near-object allocator. Hands out the `0x76`-byte object structs. `TBHEAPCLEARCRITSECT` was the last stop before a window appeared.

### Supporting
- **?SENDPROC@TBXBOBJ@@** (`29AF:0000`) — callers: GETPROC/SETPROC siblings. `cmp ax,3014`.
- Array and ref-count functions (full log only).
- **VALUENEW***, **ANSILSTRNCMPI**, **VALUECONVERT*** — fire a lot, produce flashing, not the stream walker.
