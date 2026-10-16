# 19. Heap, stack, and the resource manager

**Date:** 2026-10-16

**Status:** Side reading of `TB80BAS.DLL.c`, `TB80UTL.DLL.c`, and the 2026-10-15 WDW breakpass in `maps/wdw-to-ghidra.md`. Line numbers are the decompile. Live selectors are one boot. None of these functions is the unnamed record reader.

## Claims

| Id | Grade | Statement |
|---|---|---|
| H-001 | Known | Three allocators. UTL `GHEAP*` is one Windows global block turned into a local heap. BAS `HEAP*` / `TBHEAP*` is the NearScript frame heap. `GLOBALALLOC` of `count * 0x76` in `FUN_1278_3be6` is the live-object array. They do not call each other. |
| H-002 | Not true | "`HEAP*` / `TBHEAP*` hand out the `0x76`-byte object" and "there is no standalone `TBHEAPCLEARCRITSECT` definition." Both sentences were chapter 11. `TBHEAPCLEARCRITSECT` is decompile line 93984. No `TBHEAPALLOC` site passes `0x76`. |
| H-003 | Known | The only static caller of `HEAPREGISTER` is `RESMGRCONNECT`. It passes the second of two `MAKEPROCINSTANCE` thunks. That thunk is stored at heap `+0x20` / `+0x22` and is an indirect call. |
| H-004 | Known | The OpenScript value stack is tag `0x10` on that heap. It is not the CPU stack. A non-scalar push goes through `VALUETOSTRING` and the `CDBCHUNK*` comma split. That is why the stack and the chunk walkers shared a WDW batch. |
| H-005 | Known | `RESMGRSENDMSG` is the resource dispatcher. `RESMGRENUM` calls a `code *` argument. Five WDW return addresses that call `VALUENEWRESOURCE` and `RESMGRGETREFCNT` are still unnamed. |
| H-006 | Thought | The `0x303E`-byte heap object is the header plus a frame table of depth `0x400`. The arithmetic fits. The listing does not comment it. |

## 19.1 Three allocators

The `0x76`-byte live object is chapter 4. `CDBNEWOBJECT` indexes it as `param_6 * 0x76`. The block that holds the array is `FUN_1278_3be6` (line 121049). Empty, it `GLOBALALLOC`s `param_2 * 0x76`. Otherwise it `GLOBALREALLOC`s to the same product. The free walk at line 120992 steps `0x76`. That path does not call `TBHEAPALLOC`.

`GHEAP*` is UTL segment 9, lines 9261–9390.

| Export | What the body does |
|---|---|
| `GHEAPCREATE` | `GLOBALALLOC` of `param_2 + param_3 + 0x10`, then `GLOBALHANDLE`, then `LOCALINIT`. A non-zero `param_3` zeroes that many bytes from the symbol the listing calls `DAT_10f8_0010`. Whether that symbol is the new block was not checked. Failure calls `GHEAPDELETE`. |
| `GHEAPALLOC` | `LOCALALLOC`. |
| `GHEAPFREE` | `LOCALFREE`. |
| `GHEAPLOCK` / `UNLOCK` / `SIZE` / `REALLOC` | The matching `LOCAL*` call. |
| `GHEAPDELETE` | `GLOBALFREE` of the `GLOBALHANDLE`. |

The BAS caller is `FUN_11a8_0000` (line 82614), after `GETFREESPACE` and `GLOBALCOMPACT`. It creates two heaps, `GHEAPCREATE` with sizes `0x2002` and `0x800`, stored at `DAT_1630_03b0` and `DAT_1630_03aa`. The `0x16E0` that the decompile prints as the first argument is the same extra the listing puts on `GLOBALALLOC` and `LOCALALLOC` throughout this file. It is not a third size. `FUN_11a8_03f8` (line 82888) and `FUN_11a8_087c` (line 83240) call `GHEAPALLOC` with size `0x40`.

The UTL export trace of 53 hits included `GHEAPCREATE`, `GHEAPALLOC`, and `LOADRESSTR`. `LOADRESSTR` (UTL line 7943, segment 7) loads a Windows string resource. It is not `RESMGR*`. That trace was not a record walk. Chapter 12 already says so.

`HEAPREGISTER` itself uses `GLOBALALLOC` for the directory and for each heap object. That is the third use of the Windows allocator, and it is not `GHEAP*`.

## 19.2 The script heap

BAS segment comment "Segment 63". The functions are `FUN_11f0_*`, lines 93127–94370. The decompile passes the string `NearScript` into this family. Treat that as the module's name for the heap, not as a type check, until `FUN_11f0_2440` is read.

`HEAPREGISTER` (93127). If `DAT_1630_11ae` is null, `GLOBALALLOC` a directory of `0x2E` bytes. Word 0 is capacity, set to 10. Word 1 is the count. Word 2 is `0xFFFF`, the free-list sentinel. Each heap is `GLOBALALLOC(0x303E)`. Word 0 of the heap is magic `0xCCDD`. The first arena is `FUN_11f0_280c(0x1000)`. The caller's far pointer is stored at heap `+0x20` and `+0x22`. When the directory is full, `GLOBALREALLOC` grows the capacity by 9. The only static call is `RESMGRCONNECT` line 20089.

`HEAPDEREGISTER` (93236). If heap `+0x20` / `+0x22` is set, `FREEPROCINSTANCE` on it. Frees the arenas, unlinks the heap from the directory, and `GLOBALFREE`s the heap. Callers: the connect failure path (20127) and `RESMGRDISCONNECT` (20155).

`HEAPCREATEFRAME` (93315). Fails when the depth word at heap `+6` is `0x400`. Otherwise it carves at least `0x24` bytes from the current arena, or asks `FUN_11f0_280c` for another `0x1000`. The frame slot is `heap + depth * 10`:

| Offset | Contents |
|---|---|
| `+0x82E` / `+0x830` | Handler far pointer. `HEAPGETHANDLER` (94051) returns it. |
| `+0x832` / `+0x834` | Arena far pointer. |
| `+0x836` | Caller `BP` with the low bit cleared. `HEAPGETBPFRAME` (94063) returns it. |

`0x82E + 0x400 * 10` is `0x302E`. The error word `TBHEAPALLOC` writes is at `+0x303C`. Both sit inside the `0x303E` object. That is H-006.

`TBHEAPALLOC(size, tag, frameIndex, heap)` (93620). Adds 4 for a header. `FUN_11f0_25f8` rounds the sum. Rejects a zero round or a round `>= 0xFFC5`, and rejects a size that overflows when 4 is added. Those failures store `0x1FFF` at heap `+0x303C` and return null. The block's first word is the tag. The second word is the frame index. The pointer returned is past those four bytes. Allocation walks the frame free list (`FUN_11f0_21c4`), grows it (`FUN_11f0_1b18`), and may start a new block (`FUN_11f0_2790`). Out of memory stores `0x1F7A`. If the crit depth at heap `+0xE` is not zero, `FUN_11f0_15aa` must accept the block; otherwise the block is `TBHEAPFREE`d and the error is also `0x1F7A`.

`TBHEAPFREE` (93800). The block is the user pointer minus 4. The frame index is the word at user-minus-2. It unlinks a 4-byte entry from the table at heap `+0x18` / `+0x1A`. The scan gives up past `0x3FFF` entries. The free of the bytes is `FUN_11f0_22da`.

The crit "section" is a nesting counter, not a Win32 critical section.

| Export | Line | Effect |
|---|---|---|
| `HEAPENTERCRITSECT` | 93893 | If depth is not already `-1`, increment heap `+0xE`. Return the 32-bit cursor at `+0x10` / `+0x12`. |
| `HEAPLEAVECRITSECT` | 93909 | May write the cursor back. Decrement depth if it is not zero. |
| `TBHEAPSAVECRITSECT` | 93933 | Copy depth and the cursor, three words. |
| `TBHEAPRESTORECRITSECT` | 93953 | Write them back. A non-zero saved depth does not move the cursor backwards. |
| `TBHEAPCLEARCRITSECT` | 93984 | Zero all three words. |

`HEAPFINDCDBVALUE` (94907) calls `TBHEAPALLOC(0x5A, 0xCDBF, ...)`. The size matches the node it then fills: the last word it writes is at offset `0x58`. Every other tag in the table below is a small integer. Do not treat `0xCDBF` as a type code until those bytes are re-read. The same function's value-packing expression contains `*(uint *)0x0`, which is the decompiler losing a register.

Tags at the `TBHEAPALLOC` sites. The owner is the function whose body contains the call.

| Tag | Size argument | Owner | Line |
|---|---|---|---|
| `0` | caller size | `VALUENEW` | 85175 |
| `0` | `local_8 + 0xC` | `FUN_11d8_1a28` | 88923 |
| `0` | `(n + 3) * 4` | `FUN_1368_0de0`, the stack chunk | 154913 |
| `9` | `param_1 + 3` | `VALUENEWSTRING` | 87415 |
| `0xA` | `8` | `VALUENEWDOUBLE` | 86406 |
| `0xB` | `4` | `VALUENEWLONG` | 86282 |
| `0xC` | `4` | `VALUENEWPOINT` | 153277 |
| `0xD` | `8` | `VALUENEWRECT` | 153446 |
| `0xE` | `7` | `VALUENEWDATE` | 151703 |
| `0xF` | `3` | `VALUENEWTIME` | 151839 |
| `0x10` | `0xC` | `VALUENEWSTACK` | 154118 |
| `0x11` | `param_4 * 4 + 0x16` | `FUN_11d8_0030` | 87720 |
| `0x12` | `0x100` | `VALUENEWCOLORTABLE` | 155612 |
| `0x13` | `param_1 + 2` | `VALUENEWICON` | 153717 |
| `0x19` | `10` | `FUN_11e0_1010`, `FUN_11e0_10e0`, `FUN_11e0_11dc` | 90735, 90819, 90882 |
| `0x22` | caller size | `FUN_1390_054a`, then `HEAPADDTOCLEANUPLIST` | 157234 |

`VALUENEWCSTR` (87576) is the export in front of `FUN_11d8_0030`. The tag `0x11` call is in the helper, not in the export's own body.

## 19.3 Values, marks, and the indirect calls

A script value is not a pointer. `HEAPVALUETOPOINTER` (94011) takes the low 10 bits of the value (`value & 0x3FF`), scales by 2, and reads a selector word at `heap + index * 2 + 0x2E`. The offset half is the other argument. WDW's first instructions on that export are `and si,03FF` / `add si,si`. `HEAPVALUETOFRAME` (94020) is that lookup, then the word at the block's `-2`, which is the frame index. `FUN_11f0_0f76` checks the index is `< 0x400` and that `(block[-4] & 0x7FFF)` equals `value >> 10`.

`HEAPPOINTERTOVALUE` (94000) shifts the header word at `-4` left by 10 and mixes in a 10-bit field. The mix is the same broken `*(uint *)0x0` expression as in `HEAPFINDCDBVALUE`. The shift is in the listing. The low 10 bits of this direction are not a clean reading.

Mark and sweep:

| Function | Line | What it does |
|---|---|---|
| `HEAPMARKFRAME` | 94169 | Sets bit 7 of the byte at pointer `-3`. |
| `HEAPMARKPOINTER` | 94193 | Walks the frame's blocks. Calls `FUN_11f0_2440`. |
| `HEAPSWEEPFRAME` | 94304 | Marks the frame's pointer list, then walks the mark table through `FUN_11f0_135a`. |
| `HEAPADDTOCLEANUPLIST` | 93510 | Returns 0 unless the header word `& 0x7FFF` is `0x22`. |
| `FUN_11f0_12ac` | 94227 | If the mark bit is set, clears it and keeps the block. If the type is `0x22`, `HEAPREMOVEFROMCLEANUPLIST`, then an indirect call. |
| `FUN_1390_0596` | 157249 | The matching free: remove from the cleanup list, then `TBHEAPFREE`. |

The type-`0x22` call is not "the word at the block plus `0x2C`". `FUN_11f0_12ac` reads a far pointer from the first four bytes of the user data and calls the code pointer at that object plus `0x2C`. `FUN_1390_054a` stores the heap far pointer at user `+4` / `+6` and does not show what sits at user `+0`. The callee is unnamed.

`FUN_11f0_103c` (94071) locks the directory at `DAT_1630_11ae` and walks every registered heap. For a frame whose handler segment matches the argument, if heap `+0x20` is set, it calls that proc-instance, then `FUN_11f0_1160` may rewrite handler slots. Static callers: `FUN_10d0_07ee` (line 51677, argument 1) and `FUN_10d0_08ba` (line 51737, argument 0). The proc-instance body is the thunk `RESMGRCONNECT` registered. This pass did not name the code inside the thunk. `MAKEPROCINSTANCE` in that function is decompiled against the `CTbkSimpleOLEDispatch` string pool, which is the same artifact chapter 4 warns about. It is not evidence the thunk is an OLE method.

`FUN_1368_04ee` (154384) is the stack marker. It checks the value with `FUN_11f0_0f76`, `VALUEMARK`s each element, and `HEAPMARKFRAME`s each chunk and the header.

## 19.4 The value stack

Segment comment "Segment 110", `FUN_1368_*`, from line 154087. The context object is the script frame: heap far pointer at `+4` / `+6`, frame index at `+0xC`.

`VALUENEWSTACK` allocates the header with `TBHEAPALLOC(0xC, 0x10, frame, heap)`. Failure is `CDBSETPLERR(..., 0x1F7A, 2, ...)`. Chunks come from `FUN_1368_0de0`. A request of 0 or more than `0x19` elements becomes `0x19`. The chunk allocation is tag `0`, size `(count + 3) * 4`. Each empty slot is written as type `1`, subtype `0x400`. The header holds the count, the first chunk, and the current chunk. `HEAPPOINTERTOVALUE` writes the value back to the caller. A second chunk is linked when the fill reaches `0x19`.

| Export | Line | Behavior |
|---|---|---|
| `STACKGETSIZE` | 154518 | Type `1` and subtype `0x400` returns 0. That pair is the null value. Otherwise the count word. |
| `STACKPUSH` | 154537 | Switches on `param_2 >> 10`, the type field above the 10-bit index. |
| `STACKPUSHONE` | 154643 | If the current chunk's used count equals its capacity, `FUN_1368_0de0` allocates another. Then `VALUECOPY`. A count of `0xFFFF` is not incremented. |
| `STACKPOP` | 154759 | Empty current chunk: `CDBSETPLERR(..., 0x1FA2, 2, ...)`. Otherwise decrement, copy the slot, call `FUN_1368_1586`. An emptied chunk steps back to the previous one. |
| `STACKSLIP` | 154806 | Same `0x1FA2` on an empty chunk. Removes the front element and slides the rest down. Also calls `FUN_1368_1586`. |
| `STACKELEMENT` | 154343 | Index from the end: `count - index - 1`, via `FUN_1368_0d94`. Out of range is `CDBSETPLERR(..., 0x38, 2, ...)`. An empty slot comes back as type `1` / subtype `0x400`. |
| `STACKSETELEMENT` | 154486 | Same end-relative index, then `VALUECOPY`. |
| `STACKFREE` | 154435 | `VALUEFREE` each slot, `TBHEAPFREE` each chunk, then the header. |
| `FUN_1368_0ab8` | 154705 | Push, rotate the new elements to the front, and `STACKPOP` back to the old size on failure. |
| `FUN_1368_01d2` | 154205 | A count word of `0xFFFF` is `CDBSETPLERR(..., 0x1FFF, 2, ...)`. |

`STACKPUSH` cases `1`, `2`, `5`, `7`, `10`, `0xB`, `0x14`, `0x15`, `0x16` go straight to `STACKPUSHONE`. Cases `8` and `0xC` go through `VALUEVALUE`, then push with the low field `| 0x800`. Case `0xD` pushes three words from the pointed-to object, then one more. Case `0x10` is a stack: push each element. The default converts with `VALUETOSTRING` and calls `FUN_1368_0236` (154232), which splits the string on commas through `CDBCHUNKLAST` and `CDBCHUNKFIND`.

`FUN_1368_1586` (155393) decrements the count word unless it is already `0xFFFF`, in which case it calls `FUN_1368_1538`. The 12 October map puts the name `STACKSLIP` at `1368:1586`. This decompile has both that address-shaped function and a separate export named `STACKSLIP`. The map is a different analysis, as chapter 11 says about other offsets. Behavior above uses the decompile names. A live break uses the WDW name and the WDW offset.

The TBX wrappers that were read are one call and a return: `TBXSTACKPOP` (115944), `TBXSTACKFREE` (115955), `TBXSTACKPUSH` (116277), `TBXVALUENEWSTACK` (116288).

One boot, DGROUP `347F`, from the 17:38 batch. Same selector, one segment. The breakpass marked the whole `STACK*` set as skip. The skip was right about the reader. It was not a description of the functions.

| Export | That boot |
|---|---|
| `VALUENEWSTACK` | `4537:0000` |
| `STACKELEMENT` | `4537:0444` |
| `STACKSETELEMENT` | `4537:06B0` |
| `STACKGETSIZE` | `4537:0738` |
| `STACKPUSH` | `4537:0778` |
| `STACKPUSHONE` | `4537:09A2` |

## 19.5 The resource manager

`RESMGR*` is the book-resource manager. It is not the NE loader and not the reader.

`RESMGRCONNECT` (20043). `CDBINIT`. `LOCALALLOC` of `0xE` bytes, seven words. Two `MAKEPROCINSTANCE` thunks. `CDBCREATEINSTANCE(3, ...)` takes the first thunk. `HEAPREGISTER` takes the second. The session words are: `[0]` instance, `[1]`/`[2]` heap far pointer, `[3]`/`[4]` and `[5]`/`[6]` the two proc-instances. Failure bytes: `0x0F` if the local alloc fails, `0x0D` if `HEAPREGISTER` returns null, `0x39` (`'9'`) if a proc-instance fails. The failure path undoes whatever was created. `RESMGRDISCONNECT` (20144) destroys the instance, deregisters the heap, frees both thunks, and `LOCALFREE`s the session.

`RESMGROPENBOOK` (20177) calls `CDBCREATEBOOKREF`. `RESMGRCLOSEBOOK` (20197) calls `FUN_1048_102e` and `CDBCLEARBOOKREFS`.

`RESMGRSENDMSG` (20219) switches on the word at message `+10`.

| Case | Call |
|---|---|
| 1 | `FUN_1028_12d4`, then `FUN_1030_06a8` |
| 2 | `RESMGREXTRACT` |
| 3 | `RESMGRREPLACE` |
| 4 | `RESMGRENUM` |
| 5 | Sets a flag, then `RESMGRSENDMESSAGE` |
| 6 | `RESMGRGETNAME` |
| 7 | `RESMGRSETNAME` |
| default | Stores 1 at message `+0xC` |

`RESMGRSENDMESSAGE` is a separate export (line 21836). On the restart boot it was `3817:1C82`, `enter 0012`. Its body was not walked here.

`RESMGREXTRACT` (21513) is `FUN_1028_23ec(0, ...)`. `RESMGREXTRACTGDI` (21523) is `FUN_1028_23ec(1, ...)`. The 12 October map puts the name `RESMGREXTRACTGDI` on `1028:23EC`, which is the address form of `FUN_1028_23ec`, the shared body. The WDW stop to keep is the name plus the WDW offset: `RESMGREXTRACT` at `4D27:1710` on the first boot. The keepers table has `RESMGREXTRACTGDI` at `4D27:1730` on that same selector. `FUN_1028_23ec` itself was not read in this pass.

`RESMGRENUM` (22381) takes a `code *`. Each step calls `FUN_1008_0422`, then `(*param_4)(...)`. The loop stops when the callback returns 0, or when the status byte is nonzero. A status of `'B'` is cleared before the stop. The return is the number of steps. The 12 October map names `1008:0422` `RESMGRGETREFCNT`. In this decompile that address is the helper the enum loop calls. The export `RESMGRGETREFCNT` is a different function. Do not merge them.

Static callers of `RESMGRENUM`: `RESMGRSENDMSG` case 4, `FUN_10b0_52e8` (47305), `FUN_1300_029e` (139318 and 139350), `FUN_1308_0c2e` (140211, the decompile has the string `ACCELERATOR` at that call). The callback arguments at 47305 and 140211 are small integers in the listing (`0x5358`, `0xDEC`). Those are not named functions in this pass.

`RESMGRREPLACE` (20829) builds a message whose first word is `0x1A` and whose size word is 6, then calls `RESMGRSENDMESSAGE`. Types `0x13` and `0x10` copy two extra words into that message. `FUN_1028_0d52` calls `RESMGRGETREFCNT` only when the type word is `0x13`.

`RESMGRGETREFCNT` (22579) calls `FUN_1028_2e76`, then `FUN_1008_0438`, then `OBJUNLOCK`. `FUN_1008_0438` is the address the map labels `CDROMOBJINFO_OHANDLECHECK`. The label is the map's. The body of `0438` was not read here.

Two more indirect calls sit in this segment. `FUN_1028_2680` (22469), when a type id is `< 0x14`, calls the code pointer at that type's table entry. `FUN_1028_2770` (22535) walks `0x14` entries from `DAT_1630_0154` and calls the code pointer at `+4`. The map names `1028:2770` `RESMGROPENBOOK`. This decompile's export of that name is the `CDBCREATEBOOKREF` function at line 20177. The loop is not the open-book export.

`VALUENEWRESOURCE` is defined once, at line 90660. Nothing else in the C file calls it by that name. The callers are the WDW Calls window.

## 19.6 What the breakpass actually hit

Startup order on the first 2026-10-15 boot, heap and resource rows only. The full table is `maps/wdw-to-ghidra.md`. `TBHEAPCLEARCRITSECT` was not the last stop before the window. `VALUEFREE` was, two stops later.

| Order | That boot | Export |
|---|---|---|
| 6 | `450F:0E3E` | `TBHEAPSAVECRITSECT` |
| 9 | `450F:0E70` | `TBHEAPRESTORECRITSECT` |
| 13 | `450F:0840` | `TBHEAPALLOC` |
| 14 | `450F:0EE2` | `HEAPPOINTERTOVALUE` |
| 16 | `4D27:1710` | `RESMGREXTRACT` |
| 24 | `450F:0EC2` | `TBHEAPCLEARCRITSECT` |
| 26 | `4457:0B38` | `VALUEFREE`, before the main window |

Later the same day, still DGROUP `347F`: `HEAPCREATEFRAME` `450F:0350`, `HEAPGETHANDLER` `450F:0FEE`, `HEAPRELEASEFRAME` `450F:05D6`, `RESMGRENUM` `4D27:2522`. `HEAPRELEASEFRAME` was not read in this pass. The batch note said skip `HEAP*` and `RESMGRENUM`. That is still the right call for finding the reader.

The restart (DGROUP `2977`) hit the same offsets on a new selector. `HEAPREGISTER` `343F:0000`, `enter 0014`, compares the word at `11AE` (`DAT_1630_11ae`). `TBHEAPALLOC` `343F:0840`, `enter 0014`, `add ax,4`, which is the header. `HEAPPOINTERTOVALUE` `343F:0EE2`.

`VALUENEWRESOURCE` (`4267:0EFC`, `enter 000E`) and `RESMGRGETREFCNT` (`4D27:2838`, `enter 0008`) showed the same unnamed return addresses: `4D87:0102`, `0ED7:1E5B`, `4C0F:1C72`, `518F:4776`, `322F:180D`. The Calls note for `VALUENEWRESOURCE` also prints `4D87:01C72` and a second `0ED7:1E5B`. `4D87:01C72` is one digit away from `4C0F:1C72` and does not repeat on `RESMGRGETREFCNT`. Treat it as a bad copy of that line, not as a sixth caller, until a screenshot says otherwise. `RESMGRREPLACE` is an additional named caller of `RESMGRGETREFCNT`, which matches `FUN_1028_0d52`.

`322F` is the unnamed segment already on `CDBFILEOPEN` (`322F:3252`) and `CDBCHUNKFIND` (`322F:0577`, `322F:0E1E`). `4D87:00ED` is a caller of `VALUEARRAYCHKDIMS`. Same selector as `4D87:0102`, different offset. Do not give any of these a name.

## 19.7 What this does not name

The reader is still the unnamed walk after `CDBFILEOPEN` and before the first paint. Chapter 4. The next break is still `CDBCREATEPAGEREF` or `CDBSETVALUEEX`.

Not named here: the body of the `HEAPREGISTER` proc-instance, the type-`0x22` callee at object `+0x2C`, `FUN_1028_23ec`, `FUN_11f0_2440`, `HEAPRELEASEFRAME`, and the five `322F` / `4D87` / `0ED7` / `4C0F` / `518F` return addresses. `CDBSENDCREATE` is still author-only and was not on these Calls stacks.
