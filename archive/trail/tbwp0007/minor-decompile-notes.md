# Minor decompile notes (2026-10-14)

> Trail, 2026-10-16. Chapters 2, 5, and 17. Graphic property ids `0x4097`–`0x409B`, `LOCKPATTERN`, `layer` at `0x4059`. The page-blob slot for the bitmap id is still open. If this sheet and `TBdecompile/record/` disagree, the record wins.

From TB80BAS.DLL.html.

## Picture field

Confirmed against TBX. Pictures are not a separate object type in the sample. They are bitmap references on Button (and similar) elements:

```xml
<Button ... NormalGraphic="bitmap id 115" InvertGraphic="bitmap id 116" CheckedGraphic="bitmap id 117" .../>
```

Properties (stdprops.tsv):

```
0x4097	normalGraphic
0x4098	invertGraphic
0x4099	disabledGraphic
0x409a	stretchGraphic
0x409b	checkedGraphic
```

The id is a resource index ("bitmap id N"), not a file offset. `DRAWPICTURECALLBACK` writes the resolved GDI handle into the object at +0xC / +0xE. The id itself lives in the property block that those graphic properties point at.

## LOCKPATTERN (1098:0876)

Fill pattern lock. Called from paint paths.

- Takes a byte at `[BP+0xC]` (the pattern index).
- Range check: 1..0x80. Outside that range calls `TOOLBOOKFATAL`.
- Uses `DAT_1630_0208` / `DAT_1630_020A` as a cache.
- Paired with `UNLOCKPATTERN` (1098:09fc).

Pattern index is stored in the object (seen at +0x17 and +0x5B in the earlier .c). Not a solid color; a hatch or brush id.

## Property 0x4059

Named. Standard property resource (viewer2/stdprops.tsv):

```
0x4059	layer
```

Sits next to idNumber (0x4015) in the registrar. Not a picture id.

## RESMGREXTRACTGDI (1028:1730)

One-line wrapper. Calls `FUN_1028_23ec(1, ...)`.

### FUN_1028_23ec

Resource extract. Two paths:

- `param_2 == 0`: builds a message block and calls `RESMGRSENDMESSAGE`. Returns the result.
- `param_2 != 0`: calls `FUN_1028_2e76` to open the resource, then either `FUN_1008_0438` (if `param_1 == 0`) or `FUN_1028_341c` + `FUN_1028_32c8` (if `param_1 != 0`). The second path may `GLOBALFREE` a handle. Always `OBJUNLOCK`s before return.

Callers: `RESMGREXPORT`, `RESMGREXTRACT`, `RESMGREXTRACTGDI`, `FUN_1028_0ada`, `FUN_1028_0b9a`, `FUN_1028_0f80`, `FUN_1028_180e`, `FUN_1028_21e0`, `FUN_1028_22fe`, `FUN_1028_3e78`.

`param_1` selects the extract flavor (0 = simple, 1 = GDI). `param_2` is the resource object (0 means send a message instead).

## CDBADDBOUNDSYSBOOKS (1048:2b55)

Walks a list at `DAT_1630_0256`, count at `DAT_1630_0252`. For each entry with non-zero fields at +0xB9 / +0xBB, calls `FUN_1280_12a2`. Registers system book bounds. Not a page reader.

## CDBLOCKFONT / UNLOCKFONT (12b8:0000 / 12b8:146a)

Font resource lock.

- `CDBLOCKFONT` calls `FUN_1030_02fc` (resource open). Returns 0 on failure.
- `UNLOCKFONT` decrements a reference count at `ES:[BX + SI - 0x1c]` (SI = index * 0x45). When the count hits zero it calls `FUN_12b8_14ac` and may `SWAPSAVEDFONTS`.

Font table base is `DAT_1630_0136`. Entry size is 0x45 bytes. `nida.ttl` is the font resource; this is the lock/unlock around it.

## CDBVALUENEWKEYWORD (1078:2b18)

Keyword registration.

- Allocates a 0x400-byte buffer.
- Calls `VALUENEWKEYWORD` (1200:0186) with the keyword string and a result pointer.
- On failure calls `CDBSETPLERR`.

This is how a new OpenScript keyword is added to the runtime table. The keyword pool itself is still resource 0x77.

## HCACHESHAREDSCRIPTPURGE (10d0:2130)

Shared script cache purge.

- Walks a table at `DAT_1630_17da`.
- Count is the word at the head of that table.
- Each entry is 0x1c bytes. Skips entries whose first word is zero.
- Increments a local counter and continues until the count is exhausted.

This is why some handlers may be missing from the page blob: they were purged from the shared-script cache and not reloaded.

## Remaining open items (resolved)

### CDBCHUNKLAST (12f0:0334)

Chunk list last. Called from page readers (1238:100b, 1238:3400). Returns the index of the last chunk in a list. Writes the result into `ES:[BX+0x46]`. Used to bound a reverse walk.

### CDBCHUNKREMOVE (12f0:0550)

Chunk removal. Called from 1468:071d. Removes a named chunk from a page or object blob. Pair of `CDBCHUNKFIND` / `CDBCHUNKEND`.

### CDBCLEARBOOKREFS (1048:10a6)

Book ref cleanup. Called from 1028:0266. Walks a ref list and clears book references. Used on book close or unload.

### CDBCREATEBOOKREF (1048:0f5c)

Book ref creation. Calls `FUN_1030_02fc` (resource open) with kind 0x1. On failure returns zero. On success builds a book ref and returns the handle. Called from 1028:020f and the TBX path (11e0).

### CDBCREATEPAGEREF (1040:03b2)

Page ref creation. Calls `FUN_1048_159a` with kind 0x2. On failure returns 0 / 0x400. On success builds a page ref. Called from 1078:277e, 1088:1984, and 11e0:018c.

### CDBCHUNKEND (12f0:0000)

Chunk end finder. Enters with a length and a pointer. If the length is zero it returns immediately. Otherwise walks the buffer looking for a terminator (0x00 or a separator). Returns the offset of the end. Used by `CDBCHUNKFIND` to bound a search.

### CDBCHECKBOUNDDTL (12c8:0000)

Bounds detail check. Called from the paint path (1090:014e and three more sites). Validates the four bounds words before a draw. Not a reader; a gate.

### CDBLAYEROFVALUE (1078:06fe)

Layer reader. Returns the layer value for an object. Property 0x4059 is `layer`; this is the getter.

### CDBVALIDATEPROPERTY (1070:1774)

Property validator. Called from `CDBCHECKVERTICES`. Checks that a property id is legal for the object type. Returns early if invalid.

### DRAWICON (USER)

GDI icon draw. Called from 12d8:0670. Draws a cursor or system icon, not a content bitmap.

### TBXGETBKGNDRGBFILLCOLOR (1268:0d04)

Background fill color. Reads the page or background fill RGB. Used by the TBX export path.

### CDBCLASSTABLEGETBEHAVIOR (1280:1250)

Class behavior lookup. Returns a behavior byte for an object class. Used by the type dispatcher.
