# WDW running map — TB80BAS exports seen 2026-10-15

> Trail, 2026-10-16. Chapter 12. The spine. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: WDW screenshots during book open / page walk on Win98. Selectors are live for that boot. Function names are the NE export names WDW resolved.

## Consistent call stack (book-open / page path)

These frames appear in nearly every Calls window:

| Selector:offset | Note |
|-----------------|------|
| 0x3497:03EF | early RTM/BAS entry |
| 0x3497:4A6E | matches earlier WDW plan (F8 at 4A6E) |
| 0x3197:0379 | |
| 0x3167:0CB1 | near call |
| 0x3167:14BC | far call |
| 0x3247:02BF | near |
| 0x3247:05B7 | near |
| 0x3247:0B7A | far |

This is the spine. Everything else hangs off it.

## Functions hit (who does what)

| Live address | Export name | Role (from name + prior RE) |
|--------------|-------------|------------------------------|
| 3147:0094 | OBJGETFILE | object file access |
| 3147:0242 | OBJGETHDRLONG | object header long read |
| 4C7F:10A6 | CDBCLEARBOOKREFS | clear book references on open/close |
| 4267:02D4 | CDBVALUENEWGRAPHICREF | new graphic reference |
| 4357:02F2 | VALUEARRAYINFO | value array info |
| 450F:0F28 | HEAPVALUETOPOINTER | heap value → pointer |
| 4267:00C2 | CDBVALUENEWLAYERREF | new layer reference |
| 483F:03B2 | CDBCREATEPAGEREF | create page reference |
| 480F:04C6 | CDBCLIENTSTATUS | client status |
| 3397:147C | CDBSETVALUEEX | set property value (extended) |
| 480F:0522 | CDBREGISTERINSTWINDOW | register instance window |
| 3767:0000 | CDBREGISTEROLE2WINDOW | register OLE2 window |
| 4437:0000 | CDBREGISTERVBXFORM | register VBX form |
| 4437:0216 | VBXNEWVIEW | new VBX view |
| 4357:0932 | VALUEARRAYSET | set value array |
| 450F:0F4E | HEAPVALUETOFRAME | heap value → frame |
| 450F:0DCE | HEAPENTERCITSECT | enter critical section |
| 450F:0DF6 | HEAPLEAVECRITSECT | leave critical section |
| 4877:0000 | CDBDISPLAYSTATE | display state |
| 4877:0276 | CDBSYNCSCREENS | sync screens (known from create path) |
| 4357:05D8 | VALUEARRAYGET | get value array |
| 44CF:009E | CDBSENDSELECT | send select |
| 3397:07B2 | CDBPARENTVALUE | parent value |
| 3397:0400 | CDBDEREFVALUE | deref value |

## Not seen firing

- **CDBSENDCREATE** is listed in the Functions window but did not appear in the Calls stacks in these captures. Either the break is on the wrong segment, or object creation is going through a different entry on this path (CDBCREATEPAGEREF / CDBVALUENEW* / CDBSETVALUEEX).

## Practical next step

The spine (3497:4A6E → 3197:0379 → 3167:*) is the book-open walk. Set a break on **CDBCREATEPAGEREF** (483F:03B2 this boot) or **CDBSETVALUEEX** (3397:147C) and step into the call that builds the page. That is closer to the record reader than CDBSENDCREATE if the latter is not being hit.

Clear unused breakpoints. The "Device memory is nearly full" stop is the debugger eating RAM.

## Notes

- Selectors change per boot. The export names are stable.
- CDBSYNCSCREENS is already known as the end of the CDBSENDCREATE path. Seeing it here means some create activity is happening even if CDBSENDCREATE itself is not the entry that fired.
- VBX/OLE2 registration (CDBREGISTER*) is incidental to open; not the record reader.
