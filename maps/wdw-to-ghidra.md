# WDW selector:offset → Ghidra segment:offset

> Trail, 2026-10-16. Lookup. One boot's WDW selectors. They change on the next boot. If this file and `TBdecompile/record/` disagree, the record wins.

Source: WDW screenshots 2026-10-15. Live selectors are temporary (this boot). Offsets within the segment are stable. Map is tbworkingpapers/tbwp0002/TB80BAS.map. C decompile is Toolbook/_decompiles/TB80BAS.DLL.c.

## Resolved (in map)

| WDW (this boot) | Export | Ghidra | Notes |
|-----------------|--------|--------|-------|
| 4877:0000 | CDBDISPLAYSTATE | 1008:4B4A | display state |
| 483F:03B2 | CDBCREATEPAGEREF | 1010:211C | create page ref; calls FUN_1048_159a(...,2,...) |
| 3397:147C | CDBSETVALUEEX | 1048:2F0E | set property value; cmp [bp+0E],42 then sub ax,4000 |
| 3767:0000 | CDBREGISTEROLE2WINDOW | 1310:0292 | register OLE2 window |
| — | CDBNEWOBJECT | 12C8:0850 | object create (FUN_12c8_0850) |
| — | CDBFILEOPEN | 1028:1226 | file open |

## In C decompile, not in map (look up by name in Ghidra)

| Export | C line | Distinctive pattern from screenshot |
|--------|--------|-------------------------------------|
| CDBSYNCSCREENS | 12922 | DAT_1630_3048 = 0; DAT_1630_304a = param |
| CDBCLEARBOOKREFS | 28451 | enter 0xB8; lea ax,-2E[bp] |
| CDBCLIENTSTATUS | 25257 | push [bp+08]; push [bp+06]; push 1; call far |
| CDBREGISTERINSTWINDOW | 25296 | mov bx,[bp+0E]; mov byte [bx],0 |
| CDBREGISTERVBXFORM | 129508 | enter 6; mov bx,[bp+08]; push 1 |
| VBXNEWVIEW | 129713 | enter 8; push 011C; call far |
| VALUEARRAYINFO | 87815 | mov al,[bp+0D]; and al,FC; cmp al,44 |
| VALUEARRAYGET | 87982 | mov al,[bp+0A]; sub ah,ah |
| VALUEARRAYSET | 88133 | les bx,[bp+14]; mov ax,es:[bx+0C] |
| HEAPVALUETOPOINTER | (calls) | and si,03FF; add si,si |
| HEAPVALUETOFRAME | (calls) | push [bp+0C]; push [bp+0A]; push [bp+08]; push [bp+06] |
| OBJGETFILE | (calls) | enter 14; mov bx,[bp+0A]; mov byte [bx],0 |
| OBJGETHDRLONG | (calls) | enter 2; mov word 2862,ax |

## Call stack spine (book-open / page path)

These frames appear in nearly every Calls window. Selectors are this boot.

```
0x3497:03EF
0x3497:4A6E
0x3197:0379
0x3167:0CB1 → 0x3167:14BC
0x3247:02BF → 0x3247:05B7 → 0x3247:0B7A
```

## Practical

- Break on the Ghidra address by offset within the segment. The live selector is whatever WDW shows for TB80BAS that boot.
- CDBSENDCREATE is listed in the Functions window but did not appear in the Calls stacks. Object creation on this path is going through CDBCREATEPAGEREF / CDBSETVALUEEX / CDBVALUENEW*.
- Clear unused breakpoints. The "Device memory is nearly full" stop is the debugger.

## Next

Set the break on CDBCREATEPAGEREF (Ghidra 1010:211C) or CDBSETVALUEEX (Ghidra 1048:2F0E). Step into the call that builds the page. That is closer to the record reader than waiting for CDBSENDCREATE.

## Startup sequence (this batch)

Stops in order. VALUEFREE fired for the first time before the main window. Next batch ends at VALUETOSTRING before the file dialog.

| Order | WDW this boot | Export | Ghidra (if known) | Notes |
|-------|---------------|--------|-------------------|-------|
| 1 | 483F:041E | CDBVIEWPAGEVALUE | — | view page value |
| 2 | 343F:0876 | LOCKPATTERN | — | lock pattern |
| 3 | 3397:0958 | CDBQUERYVALUE | — | query value |
| 4 | 483F:0666 | CDBCREATEBKGNDREF | — | create background ref |
| 5 | 3397:113C | CDBSENDVALUEEX | — | send value |
| 6 | 450F:0E3E | TBHEAPSAVECRITSECT | — | heap critical section |
| 7 | 336F:0096 | CDBSCRIPTSEARCH | — | script search |
| 8 | 3397:0304 | CDBREFVALUE | — | ref value |
| 9 | 450F:0E70 | TBHEAPRESTORECRITSECT | — | restore crit |
| 10 | 4267:04E0 | CDBVALUEBOOKTOSTRING | — | book to string |
| 11 | 3397:0AAA | CDBQUERYFILEPATH | 1078:036C | query file path |
| 12 | 44D7:0000 | VALUENEWSTRING | — | new string |
| 13 | 450F:0840 | TBHEAPALLOC | — | heap alloc |
| 14 | 450F:0EE2 | HEAPPOINTERTOVALUE | — | pointer to value |
| 15 | 4877:090E | CDBSETIMAGEMEMORYMODEL | — | image memory model |
| 16 | 4D27:1710 | RESMGREXTRACT | — | resource extract |
| 17 | 3397:0612 | CDBBOOKOFVALUE | — | book of value |
| 18 | 3397:1110 | CDBSENDVALUE | — | send value |
| 19 | 4877:0506 | CDBPAINTCLIENT | — | paint client (sets 3048/304A) |
| 20 | 4877:0B6C | IMDRAWLEVELS | 1020:16DE | draw levels |
| 21 | 3AB7:0244 | CDBSETFOCUS | 1060:143E | set focus |
| 22 | 44CF:07CA | CDBSENDUNDO | — | send undo |
| 23 | 4877:09CE | IMBITBLT | — | bitblt |
| 24 | 450F:0EC2 | TBHEAPCLEARCRITSECT | — | clear crit |
| 25 | 381F:0254 | CDBRESETPLERR | — | reset error |
| 26 | 4457:0B38 | VALUEFREE | — | free value (before main window) |

## Observations

- CDBPAINTCLIENT (4877:0506) sets DAT_1630_3048 = 0 and DAT_1630_304A from the stack, same pattern as CDBSYNCSCREENS. Paint is starting before the main window.
- RESMGREXTRACT (4D27:1710) is the resource extractor. It runs before VALUEFREE.
- VALUEFREE at 4457:0B38 is the last first-time stop before the main window. The next batch ends at VALUETOSTRING before the file dialog.
- CDBSENDCREATE still has not appeared in the Calls windows. Object creation on this path is going through CDBCREATEBKGNDREF / CDBCREATEPAGEREF / CDBSETVALUEEX / CDBSENDVALUE.
- Clear unused breakpoints. The "memory and was forced to stop" message is the debugger running out of room.

## Next

The next batch ends at VALUETOSTRING (before the file dialog). Capture that sequence the same way. The record reader is still upstream of CDBSENDCREATE; these stops are the property and resource path that runs while the book is opening.

## Selector → segment mapping

The WDW selector (483F, 3397, 450F, etc.) is temporary. Windows assigns it when the NE segment is loaded. The Ghidra segment number is the NE segment index. They are not the same number.

### How to map this boot

1. In WDW, open the Module window (Window → Module, or the module list).
2. Find TB80BAS.DLL. It shows the selector for each loaded segment.
3. Or: set a break on a known function, then look at the Calls window. The return address selector is the caller's segment.
4. Once you know one selector maps to one Ghidra segment, every other function with that same selector is in the same Ghidra segment.

### Known this boot (from the screenshots)

These selectors appeared. The map offsets do not match the WDW offsets, so the map is from a different Ghidra pass. Use the WDW offset as the stable address.

| WDW selector | Seen on | Notes |
|--------------|---------|-------|
| 483F | CDBVIEWPAGEVALUE, CDBCREATEBKGNDREF | same segment |
| 3397 | CDBQUERYVALUE, CDBSENDVALUEEX, CDBREFVALUE, CDBQUERYFILEPATH, CDBBOOKOFVALUE, CDBSENDVALUE | same segment |
| 450F | TBHEAP* family | heap segment |
| 4877 | CDBSETIMAGEMEMORYMODEL, CDBPAINTCLIENT, IMDRAWLEVELS, IMBITBLT | paint/image segment |
| 4D27 | RESMGREXTRACT | resource segment |
| 4267 | CDBVALUEBOOKTOSTRING | |
| 44D7 | VALUENEWSTRING | |
| 44CF | CDBSENDUNDO | |
| 3AB7 | CDBSETFOCUS | |
| 381F | CDBRESETPLERR | |
| 4457 | VALUEFREE | |
| 336F | CDBSCRIPTSEARCH | |
| 343F | LOCKPATTERN | |

### Practical

- The offset is what matches Ghidra. If the map offset does not match the WDW offset, the map is from a different analysis. Use the WDW offset and the function name.
- To get a fresh map, re-export the Ghidra symbol map from the current analysis.
- Clear unused breakpoints. The debugger is running out of memory.

## Method (this boot)

For each first-time stop we have:

- WDW selector (temporary, changes next boot)
- Function name (stable)
- Offset within the segment (stable)
- First instructions (stable pattern)

Match later by name + offset + instruction bytes. Do not re-scan the whole Functions list. The Calls window already shows the return address of the caller; that is the next place to look if the function is not named.

If the session is restarted, the selector changes. The offset and the instruction bytes do not. Match on those.

## What we have this boot

See the table above. The map offsets do not match the WDW offsets, so the map is from a different analysis. Use the WDW offset and the function name. Re-export the Ghidra symbol map from the current analysis to get fresh offsets.

## Batch 2026-10-15 17:38–17:46

| Function | WDW selector:offset | Segment group | Notes |
|----------|---------------------|---------------|-------|
| VALUETOSTRING | 4457:0DE8 | 4457 | value convert |
| OBJFILEOPEN | 3147:177C | 3147 | file open |
| STACKGETSIZE | 4537:0738 | 4537 | stack |
| VALUENEWSTACK | 4537:0000 | 4537 | stack |
| STACKPUSH | 4537:0778 | 4537 | stack |
| CDBCHUNKLAST | 0D37:0334 | 0D37 | chunk walk |
| CDBCHUNKEND | 0D37:0000 | 0D37 | chunk walk |
| STACKPUSHONE | 4537:09A2 | 4537 | stack |
| STACKELEMENT | 4537:0444 | 4537 | stack |
| STACKSETELEMENT | 4537:06B0 | 4537 | stack |
| VALUENEW | 4457:0C6E | 4457 | value |
| VALUEAS | 4457:0038 | 4457 | value |
| VALUEASEX | 4457:00A0 | 4457 | value |
| RESMGRENUM | 4D27:2522 | 4D27 | resource enum |
| CDBLOCKVALUE | 3397:02CA | 3397 | value lock |
| HEAPCREATEFRAME | 450F:0350 | 450F | heap |
| VALUEASC | 4457:01B8 | 4457 | value |
| VALUEASCEX | 4457:0220 | 4457 | value |
| VALUECONVERTTOC | 4457:0818 | 4457 | value |
| VALUECONVERTTOCEX | 4457:0880 | 4457 | value |
| VALUEFROMSTRING | 4457:0E1A | 4457 | value |
| CDBSETPLERR | 381F:0010 | 381F | error |
| LPSTRTODOUBLE | 4477:05B4 | 4477 | string→double |
| HEAPGETHANDLER | 450F:0FEE | 450F | heap |
| VALUECHECK | 44FF:0000 | 44FF | value |
| CDBCHUNKFIND | 0D37:0146 | 0D37 | chunk walk |
| HEAPRELEASEFRAME | 450F:05D6 | 450F | heap |
| VALUENEWLAYEREX | 4267:127A | 4267 | value |
| VALUEATOL | 443F:0000 | 443F | value |
| ANSILSTRNCMPI | 2A8F:00D3 | 2A8F | string compare |
| ?SENDPROC@TBXBOBJ@@... | 29AF:0000 | 29AF | ActiveX/OLE |
| VALUENEWTIME | 449F:01C0 | 449F | value |

### Selector groups this batch

- **4457**: VALUETOSTRING, VALUENEW, VALUEAS, VALUEASEX, VALUEASC, VALUEASCEX, VALUECONVERTTOC, VALUECONVERTTOCEX, VALUEFROMSTRING (value conversion cluster)
- **4537**: STACKGETSIZE, VALUENEWSTACK, STACKPUSH, STACKPUSHONE, STACKELEMENT, STACKSETELEMENT (stack cluster)
- **0D37**: CDBCHUNKLAST, CDBCHUNKEND, CDBCHUNKFIND (chunk walkers)
- **450F**: HEAPCREATEFRAME, HEAPGETHANDLER, HEAPRELEASEFRAME (heap)
- **4D27**: RESMGRENUM (resource)
- **3397**: CDBLOCKVALUE (same selector as earlier CDBQUERYVALUE family)
- **381F**: CDBSETPLERR
- **4477**: LPSTRTODOUBLE
- **44FF**: VALUECHECK
- **4267**: VALUENEWLAYEREX
- **443F**: VALUEATOL
- **2A8F**: ANSILSTRNCMPI
- **29AF**: ?SENDPROC@TBXBOBJ@@ (ActiveX)
- **449F**: VALUENEWTIME

### Useful vs noise

Most of this batch is value conversion and stack machinery. Not on the book-open or paint path.

**Worth keeping:**
- CDBCHUNKFIND / CDBCHUNKEND / CDBCHUNKLAST (0D37) — chunk walkers. These walk the property/record chunks. Related to the 14 00 00 reader question.
- CDBLOCKVALUE (3397) — same selector as the earlier CDBQUERYVALUE / CDBSENDVALUEEX family. Value locking.
- OBJFILEOPEN (3147) — file open path.
- ?SENDPROC@TBXBOBJ@@ (29AF) — ActiveX/OLE send. Side quest.

**Skip for now:**
- All STACK* (4537) — stack machine.
- All VALUE* convert/as/check (4457, 44FF, 443F, 4267, 449F) — value type conversion.
- HEAP* (450F) — heap frames.
- ANSILSTRNCMPI (2A8F) — string compare.
- RESMGRENUM (4D27) — resource enum.
- LPSTRTODOUBLE (4477) — string to double.
- CDBSETPLERR (381F) — error set.

The chunk walkers (CDBCHUNK*) are the closest thing to a record reader in this batch. They are not the 14 00 00 reader, but they walk the property chunks that sit inside the page records.

## Callers and first instructions (this batch, interesting ones)

### CDBCHUNKFIND (0D37:0146)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov ax,word ptr 12[bp] / sub ax,0001 / sbb cx,cx / not cx
- Callers visible: 4857:0C68 (????), 4857:090B (call near), 3187:0210 (call far), 322F:0577 (cmp ax,268), 322F:0E1E (jmp word)

### CDBCHUNKEND (0D37:0000)
- First: mov ax,347F / enter 0004,00 / push si / push ds / mov ds,ax / mov word ptr -02[bp],0 / cmp word ptr 0C[bp],00 / jne 003E
- Callers visible: 3187:0210 (call far), 0D37:2B77 (????), 0D37:12BC (????), 0D37:247E (????), 0D37:0AE5 (????), 0D37:07FB (????), CDBCHUNKFIND (jb 0x0297)

### CDBCHUNKLAST (0D37:0334)
- First: mov ax,347F / enter 0010,00 / push si / push ds / mov ds,ax / xor ax,ax / mov word ptr -04[bp],ax / mov word ptr -06[bp],ax
- Callers visible: 4857:090B (call near), 4857:0B23 (call dword), 3187:0210 (call far), CDBCHUNKEND (leave)

### CDBLOCKVALUE (3397:02CA)
- First: mov ax,347F / enter 0002,00 / push ds / mov ds,ax / mov al,byte ptr 0B[bp] / shr al,02 / sub ah,ah / sub ax,001A
- Callers visible: 4857:4FF6 (????), 4857:0C68 (call dword), 4857:42B8 (????), 4857:090B (call near), 3187:0210 (call far), 31B7:0073 (call near), 31B7:00F9 (call near)

### OBJFILEOPEN (3147:177C)
- First: mov ax,347F / enter 025A,00 / push di / push si / push ds / mov ds,ax / mov word ptr -04[bp],...
- Callers visible: 322F:3252 (jmp 0x31FC), 3D6F:0416 (call near), 3D6F:0F79 (call near), 3D6F:0E8E (call far), 3247:0219 (call near), 3247:25A7 (call far), OBJGETFILE, OBJFREESEG

### ?SENDPROC@TBXBOBJ@@ (29AF:0000)
- First: mov ax,347F / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / cmp ax,3014 / jne 0014
- Callers visible: ?GETPROC@TBXBOBJ@@, 29AF:033CE, ?SETPROC@TBXBOBJ@@, SENDPROC@TBXBOBJ@@ (self), 29AF:0206D, ?SETPROC@TBXBOBJ@@

### Matching note
For next boot, match these by function name + first instruction bytes (mov ax,347F is the common entry, then the enter size differs). The 347F is this boot's DGROUP. It will change. The enter size and the next instructions are stable.

## Callers and first instructions (batch 2026-10-15 18:16, interesting ones)

### CDBCLASSTABLEGETBEHAVIOR (44F7:121A)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / cmp word ptr 08[bp],00 / je 129A
- Callers visible: 3197:08A3, 3197:0C3F, 3197:105C, 3CC7:0379, 44F7:026A, 44F7:3FEF
- Note: Unbreaking this let the splash page run. Hit during book open / class-table setup.

### CDBVALUENEWBOOKREF (4267:0000)
- First: mov ax,347F / enter 0004,00 / push ds / mov ds,ax / mov ax,word ptr 08[bp] / or ax,word ptr 06[bp]
- Callers visible: 3467:19AD, 3467:1333, 3467:0B0F, 322F:0E1E, 322F:180D

### VALUENEWGRAPHIC (4267:1494)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov al,byte ptr 11[bp] / and al,FC
- Callers visible: 3467:1934, 3467:1176, 3467:0B0F, 322F:0E1E, 0DC7:1C82, 516F:044B

### VALUENEWBOOK (4267:0D90)
- First: mov ax,347F / enter 0006,00 / push ds / mov ds,ax / mov word ptr -06[bp],0
- Callers visible: 3D6F:0EDF, 3467:0369, 3467:19AD, 3467:1333, 3467:0B0F, 322F:0E1E

### GETDIBCOLORCOUNT (35D7:053A)
- First: mov ax,347F / enter 0006,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp]
- Callers visible: PATTERNDITHER_8BIT, CREATEDITHEREDHEADER_8BIT, GETDIBSIZE, CREATEDIBMASK (self-cluster)

### HUGEGETDATA (33BF:0D6C)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / mov word ptr -04[bp],0
- Callers visible: 33BF:1140, 33BF:02AB, 33BF:0118, 33BF:2CF2, 33BF:0F64, 33BF:0A64, 33BF:0AAD

### OBJREALLOCNEAR (3147:08D6)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp]
- Callers visible: 322F:170F, 409F:0890, 409F:2241, OBJNEWNEAREX, OBJFILECOPY, OBJGETHDRLONG, OBJFREENEAR

### Matching note
Same as prior batches: mov ax,347F is this boot's DGROUP and will change. Match on enter size and the next 2-3 instructions. CDBCLASSTABLEGETBEHAVIOR is the splash-gate observation for this batch.

## Callers and first instructions (batch 2026-10-15 18:22, interesting ones)

### CDBCREATEINSTANCE (480F:0000)
- First: mov ax,347F / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp]
- Callers visible: 4EDF:0067, 0D67:87A2, 322F:170F, 40A7:167A, 40A7:1628, 3DE7:029B, 315F:0231

### CDBVALUEBOOKFROMSTRING (4267:03F4)
- First: mov ax,347F / enter 0018,00 / push si / push ds / mov ds,ax / push word ptr 08[bp]
- Callers visible: 4267:1E8F, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWGRAPHIC

### CDBVALUEGRAPHICFROMSTRING (4267:0AA0)
- First: mov ax,347F / enter 0074,00 / push si / push ds / mov ds,ax / mov word ptr -44[bp],0
- Callers visible: CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK

### CDBVALUELAYERFROMSTRBOOK (4267:05F8)
- First: mov ax,347F / enter 004C,00 / push si / push ds / mov ds,ax / mov word ptr -2C[bp],0
- Callers visible: CDBVALUENEWLAYERREF, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWLAYER
- Note: User goofed on CDBVALUELAYERFROMSTRING; two screenshots of this function.

### CDBVALUERESOURCEFROMSTRING (4267:08B2)
- First: mov ax,347F / enter 004A,00 / push ds / mov ds,ax / mov word ptr -2C[bp],0
- Callers visible: CDBVALUEBOOKTOSTRING, CDBVALUENEWBOOKREF, CDBVALUENEWLAYERREF, CDBVALUENEWGRAPHICREF, CDBVALUELAYERFROMSTRBOOK, VALUENEWBOOK, VALUENEWRESOURCE

### Matching note
Same as prior batches: mov ax,347F is this boot's DGROUP and will change. Match on enter size and the next 2-3 instructions.

## Callers and first instructions (batch 2026-10-15 18:32, app now paging)

### GETDIBSIZE (35D7:05DA)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp]
- Callers visible: 35D7:113E (PATTERNDITHER_8BIT), CREATEDITHEREDHEADER_8BIT, 35D7:5EC2, 35D7:4FE5, 35D7:5134, 35D7:197E

### VALUEARRAYCHKDIMS (4357:03D8)
- First: mov ax,347F / enter 0022,00 / push ds / mov ds,ax / mov al,byte ptr 0B[bp]
- Callers visible: 3467:1333, 3467:0B0F, 322F:0E1E, 4DEF:013B, 4D87:00ED, 516F:52BD, 322F:1689

### VALUENEWRESOURCE (4267:0EFC)
- First: mov ax,347F / enter 000E,00 / push di / push si / push ds / mov ds,ax / cmp word ptr 0A[bp],00
- Callers visible: 4D87:0102, 0ED7:1E5B, 4D87:01C72, 0ED7:1E5B, 4C0F:1C72, 518F:4776, 322F:180D

### RESMGRGETREFCNT (4D27:2838)
- First: mov ax,347F / enter 0008,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp]
- Callers visible: 4D87:0102, 0ED7:1E5B, 4C0F:1C72, 518F:4776, 322F:180D, RESMGRREPLACE

### Status note
After this batch the application is up and paging through the book without re-breaking. Splash gate and early constructors have been passed.

## Callers and first instructions (batch 2026-10-15 18:39, menu break)

### COLORHLSTORGB (44B7:0B84)
- First: mov ax,347F / enter 0034,00 / push di / push si / push ds / mov ds,ax / mov ax,word ptr 08[bp] / or ax,word ptr 06[bp] / jne 0BBE / push 0000
- Callers visible: 516F:2ED4, 44B7:1FF7, VALUENEWCOLORTABLE, VALUENEWCOLOR
- Behavior: fired when menu was drawn. Unbreaking returned to the menu. HLS-to-RGB color helper, supporting graphics. Not a gate.

## Callers and first instructions (batch 2026-10-15 18:42, Lesson Exit)

Successful exit. Cleanup paths only.

### CDBUNREGISTERVBXFORM (4437:0068)
- First: mov ax,347F / enter 0002,00 / push ds / mov ds,ax / mov bx,word ptr 08[bp] / mov byte ptr ss:[bx],0 / push bx / push word ptr 06[bp] / push 0001 / call far ptr 4857:02FC
- Callers visible: 3197:03F8, 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX

### VBXDESTROYVIEW (4437:02F0)
- First: mov ax,347F / enter 000E,00 / push ds / mov ds,ax / les bx,dword ptr 06[bp] / mov word ptr -04[bp],bx / mov word ptr -02[bp],es / mov word ptr es:02[bx] / mov ax,word ptr es:06[bx] / or ax,word ptr es:04[bx]
- Callers visible: 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX

### CDBDESTROYINSTANCE (480F:040A)
- First: mov ax,347F / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 08[bp] / push word ptr 06[bp] / push 0003 / call far ptr 4857:02FC
- Callers visible: 31EF:1DFD, DISPATCHINPUT, CALLNEXTHOOKEX, 315F:2094, 315F:1194

### Status note
These fire during Lesson Exit. Supporting cleanup (VBX and instance teardown). Not open/render keepers.

## Callers and first instructions (batch 2026-10-15 18:44-18:51, restart)

Segment changed on restart. Object/heap/value init paths. Supporting only.

### HEAPREGISTER (343F:0000)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / cmp word ptr 11AE,0000 / jne 004C / push 2042 / push 0000 / push 002E

### VALUEINIT (44CF:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / les bx,dword ptr 06[bp] / sub ax,ax / mov word ptr es:B0[bx] / mov word ptr es:AE[bx] / mov word ptr es:08[bx]

### VALUENEWARRAY (395F:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 16[bp] / push word ptr 14[bp] / push word ptr 12[bp] / push word ptr 10[bp] / push word ptr 0E[bp]

### TBHEAPALLOC (343F:0840)
- First: mov ax,2977 / enter 0014,00 / push di / push si / push ds / mov ds,ax / mov ax,word ptr 06[bp] / add ax,0004 / cmp ax,word ptr 06[bp] / jae 085A

### HEAPPOINTERTOVALUE (343F:0EE2)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / mov cx,word ptr 06[bp] / mov word ptr -04[bp],cx / mov ax,word ptr 08[bp] / mov es,ax / mov ax,word ptr -02[bp] / mov cx,ax

### CDBINIT (37A7:0000)
- First: mov ax,2977 / enter 00C8,00 / push di / push si / push ds / mov ds,ax / mov bx,word ptr 06[bp] / mov byte ptr ss:[bx],0 / push bx / call far ptr 2A9F:0000

### OBJINIT (4357:0000)
- First: mov ax,2977 / enter 0016,00 / push ds / mov ds,ax / cmp word ptr 034C,0000 / jne 0054 / call far ptr 34F7:0E58 / mov word ptr -08[bp],dx / or dx,ax / je 002D

### VALUENEWSTRING (3397:0000)
- First: mov ax,2977 / enter 0004,00 / push di / push ds / mov ds,ax / cmp word ptr 06[bp],00 / jne 0028 / mov ax,word ptr 0A[bp] / or ax,word ptr 08[bp]

### CDBCREATEINSTANCE (4387:0000)
- First: mov ax,2977 / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp] / mov byte ptr ss:[bx],0 / cmp word ptr 018C,0000 / jne 0028 / mov bx,word ptr 0E[bp]

### CDBREFVALUE (3B6F:0304)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / cmp word ptr 06[bp],00 / jne 0326 / cmp word ptr 08[bp],04 / jne 0326 / mov ax,word ptr 06[bp]

### CDBFILENEW (3B5F:0028)
- First: mov ax,2977 / enter 0022,00 / push ds / mov ds,ax / push word ptr 0E[bp] / push word ptr 0C[bp] / push 0001 / call far ptr 3877:02FC / or ax,ax / jne 0046

### OBJNEWSEG (4867:06E6)
- First: mov ax,2977 / enter 000E,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / mov word ptr 2862,ax / mov word ptr -02[bp],ax

### OBJLOCK (4867:0308)
- First: mov ax,2977 / enter 0006,00 / push ds / mov ds,ax / push word ptr 0C[bp] / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / call far ptr 3AB7:0000 / or ax,ax

### OBJNEWNEAR (4867:0552)
- First: mov ax,2977 / enter 0008,00 / push di / push si / push ds / mov ds,ax / mov bx,word ptr 0E[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0C[bp] / mov dx,ax

### LOOKUPSTDPROPBYNAME (337F:010A)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 08[bp] / push word ptr 06[bp] / push word ptr 19FC / push word ptr 19FA / push cs

### OBJTOUCH (4867:0AD4)
- First: mov ax,2977 / enter 0024,00 / push si / push ds / mov ds,ax / mov ax,word ptr 0A[bp] / or ax,word ptr 08[bp] / jne 0AF0 / xor ax,ax / cwd

### OBJOPTOOH (4867:01DA)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / push word ptr 06[bp] / push cs

### OBJOOTOOH (4867:0176)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx / mov es,ax

### OBJNEWNEAREX (4867:0606)
- First: mov ax,2977 / enter 0022,00 / push si / push ds / mov ds,ax / mov bx,word ptr 10[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0E[bp] / sub bx,bx / mov es,ax

### OBJFREENEAREX (4867:0E36)
- First: mov ax,2977 / enter 0016,00 / push si / push ds / mov ds,ax / mov word ptr -04[bp],0 / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx

### SENDPROC@TBXUSER (33DF:0000)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / sub ax,ax / mov word ptr -02[bp],ax / mov word ptr -04[bp],ax / mov ax,word ptr 0E[bp] / sub ax,000A / je 004E

### OBJPRINCIPALOO (4867:0A40)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / push word ptr 0A[bp] / push word ptr 08[bp] / push word ptr 06[bp] / push cs / call near ptr OBJPRINCIPALOP

### OBJPRINCIPALOP (4867:0A5C)
- First: mov ax,2977 / enter 0012,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / sub bx,bx / mov es,ax

### SENDPROC@TBXBASE (59DF:0000)
- First: mov ax,2977 / enter 002E,00 / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / cmp ax,3012 / je 0064 / ja 0026 / sub ax,000A / je 0038

### HCACHEPURGE (3787:0690)
- First: mov ax,2977 / enter 0038,00 / push ds / mov ds,ax / cmp word ptr 17E2,0000 / jne 06A4 / jmp near ptr 07EA / mov ax,word ptr 17DC / or ax,word ptr 17DA / jne 06B0

### SETPROC@TBXBASE (59DF:00F4)
- First: mov ax,2977 / enter 0004,00 / push ds / mov ds,ax / mov bx,word ptr 14[bp] / xor ax,ax / mov byte ptr ss:[bx],7 / cwd / pop ds / leave

### OBJUNLOCK (4867:0432)
- First: mov ax,2977 / enter 004A,00 / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / mov word ptr -4A[bp],ax / sub bx,bx / mov es,ax

### OBJARENACHECK (4397:0AE2)
- First: mov ax,2977 / enter 002A,00 / push ds / mov ds,ax / mov word ptr -02[bp],0 / mov ax,word ptr 14[bp] / sub cx,cx / mov word ptr -06[bp],cx / mov word ptr -04[bp],ax / mov bx,cx

### OBJGETFILE (4867:0094)
- First: mov ax,2977 / enter 0014,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / sub bx,bx / mov es,ax

### SENDPROC@TBXLAYER (344F:0000)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / sub ax,302E / je 0048 / sub ax,006A / je 005E

### SETPROC@TBXLAYER (344F:0156)
- First: mov ax,2977 / push bp / mov bp,sp / push ds / mov ds,ax / mov ax,word ptr 0E[bp] / sub ax,401B / je 0194 / sub ax,000F / je 01AC

### OBJGETHDRLONG (4867:0242)
- First: mov ax,2977 / enter 0002,00 / push si / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 08[bp] / mov word ptr 2862,ax / mov word ptr -02[bp],ax

### RESMGRSENDMESSAGE (3817:1C82)
- First: mov ax,2977 / enter 0012,00 / push si / push ds / mov ds,ax / sub ax,ax / mov word ptr -10[bp],ax / mov word ptr -12[bp],ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],ax

### CDBCLEARBOOKREFS (3B5F:10A6)
- First: mov ax,2977 / enter 00B8,00 / push ds / mov ds,ax / mov bx,word ptr 0A[bp] / mov byte ptr ss:[bx],0 / lea ax,-2E[bp] / push ss / push ax / call far ptr 3877:0000

### CDBCREATEBOOKREF (3B5F:0F5C)
- First: mov ax,2977 / enter 000E,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / push bx / push word ptr 0A[bp] / push 0001 / call far ptr 3877:02FC

### CDBGETVALUEEX (3B6F:0D80)
- First: mov ax,2977 / enter 0038,00 / push ds / mov ds,ax / mov word ptr -12[bp],0 / sub ax,ax / mov word ptr -14[bp],ax / mov word ptr -16[bp],ax / mov word ptr -18[bp],ax / mov word ptr -10[bp],0

### OBJLOCKNEAR (4867:03D6)
- First: mov ax,2977 / enter 000E,00 / push ds / mov ds,ax / mov bx,word ptr 0C[bp] / mov byte ptr ss:[bx],0 / mov ax,word ptr 0A[bp] / sub bx,bx / mov es,ax / mov ax,word ptr es:0000

### CDBVALUENEWGRAPHICREF (33EF:02D4)
- First: mov ax,2977 / enter 0024,00 / push ds / mov ds,ax / lea ax,-02[bp] / push ax / push word ptr 10[bp] / push word ptr 0E[bp] / push word ptr 0C[bp] / push word ptr 0A[bp]

### Status note
Object management, heap, and value creation. Supporting infrastructure for book open. Not open/render keepers. Segment changed on restart.
