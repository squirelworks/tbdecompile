# 17. Modules

Eight modules were counted for pattern coverage on 2026-10-11: 10,991 unique functions, 1,918 nameable by pattern (17.5 percent). Confirmed renames after the later digs are 112: BAS 20, BMP 14, RTM 9, and the rest across CMP, UTL, W16, LNL, MM, RCR, FLT, NET, JPG, and VBX. Pattern coverage: RTM 32.7 percent, UTL 41.1, BMP 26, BAS 17.4, W16 17.3, LNL 12.2, CMP 5.6. A pattern name is a candidate. The scripts in `rename/` are what was applied. Naming another thousand `StrCpy` wrappers will not find the record reader.

## 17.1 Launch

| Piece | What it is | What it is not |
|---|---|---|
| `TB80RUN` | 32-bit launcher. Spawns `TB80NET.EXE` with the book on the command line. | Not an in-process thunk, and not the parser. |
| `TB80NET.EXE` | 16-bit NE. Network provider: zlib, `TBKNET3WNDPROC`, `TBK.INI`. Class `TbkNet3TB80`. | Does not parse pages. |
| `TB80RTM.EXE` | 16-bit shell. `TBKMain`, `TBKClient`, `TBKChildWindow`, `TBKReserved_1`, `SchedulerWndTB80`. `WM_PAINT` calls `CLIENTTOPAGE`, then BAS ordinal 26. | Does not draw shapes. A lesson click arrives on `TBKClient`, not `TBKChildWindow`. `BMSG` does not see that queue. |
| `TB80MAIN.EXE` | 23552-byte 32-bit stub. Calls `TB80RMT CreateRemoteCallServer` and pumps keys. Failure text: "TB80MAIN: Loading ActiveX support failed." | Not the book engine. |
| `tbload.exe` | Finds `ZZZTBKBOOKLOC` via `MINSTB32.dll` (`FUN_00405460`). Virtual call at `00406aa1` inside `FUN_00406a70` (vtable+4). | The callee is unresolved. Thought: first handoff out of the 32-bit search. |
| `TB80W32.DLL` / `TB80W16.DLL` | Thunk halves, about 246 and 406 exports. W16 is also the `DoCmd*` bus (`DoCmdDraw`, `DoCmdMouseDown`). | W16 setup (platform, OLE, 32-bit `LoadLibrary`) is not book open. |
| `TBFILE32.DLL` | Long filenames for the 16-bit engine. | |
| `TB80F32L.dll` | Flat 32-bit entry and the common-dialog hook. | |
| `TB80RMT` | Remote-call server used by `TB80MAIN`. | Not on the path that opens a lesson. |
| `PHYSSIZE` | A 1.5-era index. | Not in these 8.1 books. |

The engine calls 16-bit `USER`, `GDI`, and `KERNEL`. A log that says `USER32` is missing is not a broken install. The images in hand are 16-bit NE. ToolBook 9.0 is the 32-bit product. A correspondent's claim that 8.1 is 32-bit and needs Windows 10 is rejected by the binaries (claim C-006).

## 17.2 Book server and neighbors

| Module | Role | Not |
|---|---|---|
| `TB80BAS.DLL` | Objects, properties, painters, twip scale, file open. 606 exports. `CDBINIT` ordinal 1, `CDBFILEOPEN` 8, `CDBVIEWPAGE` 15, `CDBVIEWBKGND` 18, `CDBPAINTCLIENT` 26, `CDBSENDCREATE` 51 (author). The `CDB*` / `OBJ*` split is chapter 20. | Not the window. |
| `TB80CMP.DLL` | Compile and expand. Resources `0x77`, `0x78`, `0x70`. | Not the page walker. 5.6 percent pattern-nameable because it is a compiler. |
| `TB80UTL.DLL` | Type-name strings, string manager, metrics, heaps. | Not the `14 00 00` reader. |
| `TB80RCR.DLL` | Controls, mouse hook, effect objects, button drawing. Init is `FUN_1010_0000`. | Not classified as the book reader. The init does not open a file. |
| `TB80ENU1` / `ENU2` | English strings, 16-bit and 32-bit. | Not code that opens a book. |
| `TB80BMP.DLL` | DIB, metafile, FX blit. Ordinal 3 is the bitmap reader. `Lz77Expand` is `FUN_1000_0031`. | Not a picture store. The widget still does not name the bitmap. |
| `TB80JPG.DLL` | JPEG. Version resource still says `TB60JPG.DLL`. | |
| `TB80LNL.DLL` | MCI, wave, MMIO. The notify callback is Lionel. | |
| `TB80MM.DLL` | `tbkmmNotify`, `imageNotify`, `mciNotify`, `timerNotify`. | Does not classify objects. |
| `TB80OLE` / `OCX` / `ACX` / `VBX` | Clipboard, controls, automation. | Not on the Logic Families paint path. |
| `TB80FLT` | Filter registration. `FUN_1028_2680` calls `TBREGISTERFILTER`. The `0x14` there is a type-code limit. | Not the reader. |
| `TB80RCA.DLL` | Author UI widgets. | Not book open, not the cipher. |
| `TBCBT.DLL` | CBT scoring. Segment 7 is the cipher (chapter 16). | Not the reader. Not loaded as segment 7 in the session that listed the other code segments. |
| `TBDLG`, `TBWIN`, `TBDOS`, `TBREG`, `TBDB3`, `TBPDX` | `linkDLL` commands. | Not page walkers. |
| `DIBUTIL.DLL` | DIB helper beside BMP. | Not the object format. |

Author binaries `TB80EDT.DLL` and `TB80.EXE` are not in this set. The runtime half of the author contract is visible: BAS exports `CDBEDITBOOK`, `CDBVIEWBOOK`, `CDBISVIEWERINGENERICEDITMODE`, `CDBSENDEDITLEAVETOALL*`, and `TBXAUTHORMODE`. RTM calls `GETAUTHORLOCALIZEDDLL`. `TB80ATH.EXE` is the 16-bit author, seen under NTVDM. That is bookmarked, not solved.

## 17.3 Closed as the reader

| Candidate | What it actually is |
|---|---|
| `CDBSENDCREATE` (ordinal 51, `12c8:00BC`) | Author create and rewrite. |
| `FUN_12c8_0ef8` | Copies four words on that author path. The source is not the disk record. |
| `FUN_1028_2680` | Filter registrar. |
| `FUN_1008_2d31` (switch `1008:2DC7`) | OpenScript math. |
| `TB80RTM` | Paint handoff only. |
| `CDBCHUNKFIND` / `LAST` / `END` / `CDBSKIPSEP` | Text separators. |
| `VALUENEWLONG` and the `4267` constructors | Value constructors. |
| `FUN_10b0_00a6` | Type dispatcher. Code `0x14` is a type code. |
| `12e8:0000` | OLE object clone. |
| BAS segment 182 | 39 far calls with a zero segment and no reloc. Not book open. |
| BAS segments `1018`, `1278`, `1478`, `14b8`, `1508`, `10d0`, `1030`, `14a8`, `1160`, `1070` | Sampled. No stream walker. `1160` is debugging (`CDBGETNEURONURL`, `CDBATTACHBREAKADDRESS`). `1018` creates pens, brushes, and bitmaps. |
| A static search for the bytes `14 00 00` | Thirteen undisassembled runs contain the word `14 00` as immediates, `MOV CX, 0x14`, or jump displacements. Not a far-pointer compare that builds an object. |

## 17.4 Ghidra

Two NE loader bugs were fixed for this work: the entry-table segment byte was treated as signed, and `ne_cbenttab` was ignored. `TB80BAS` is the image with entry segment bytes at or above 128. `toolbookunpacker` clears the Optloader self-load flag and does not patch the entry table. The Ghidra patch does. An honest BAS image loads in the patched Ghidra 12.1.4 build.

Force-disassemble: walk undefined `C8` (`ENTER`) bytes first, then the prologue pass. The prologue pass accepts a real `RET` / `RETF` before treating the following byte as code, and it only creates functions at entry-like symbols. They do not name anything.

`SENDMESSAGE` (321 hits in one RTM listing) and `LSTRLEN` (282) have mangled arguments. That is a decompiler problem. It wants a fresh decompile, not another reading of the same HTML.

`maps/bas-ne-to-ghidra.md` and `maps/rtm-ne-to-ghidra.md` are the segment crosswalks. `maps/wdw-to-ghidra.md` is one boot's selectors. None of the three is a narrative. Appendix K of the reference manual is the procedure those maps belong to.

## 17.5 RCR, from the 16 October stop

There is no separate HTML listing. The decompile is `Toolbook/_decompiles/TB80RCR.DLL.c`. It has 293 functions: 191 still named `FUN_`, 53 `ASYMTBKFX*`, 13 `ASYMCTL*`, 10 `BMR*`, 8 `ASYMMTRK*`, plus help, `WEP`, and `BTNPROCBITMAPBUTTONPROC`. The Watcom list is that export set. The names are definitions in this file, not unnamed functions waiting to be matched.

The stop was `TB80RCR.DLL`, selector `3C4F`. `ASYMTBKFXINIT` at `493A` is the decompile at line 25267: `FUN_1008_aa62`, then return 1. The far call `43EF:AA62` is that first call. `ASYMMTRKINIT` at `2E0A` is line 23315. The `cmp` of word `0044` is `DAT_1020_0044`. Zero means first time. The following `push 2042h` is the `GLOBALALLOC` flags. The listing allocates `0x84` bytes, locks them, registers two window messages, and calls `SETWINDOWSHOOKEX`.

Those two are not the first instructions of the DLL. `entry` (line 9587) does `LOCALINIT`, `GETVERSION`, and `int 21h`, then `FUN_1008_d7ca`, which calls `FUN_1010_0000`. That function's order is `LOCALINIT`, `HELPINIT`, `ASYMTBKFXINIT`, `ASYMMTRKINIT`, and if the mouse init returns 0, `FUN_1010_c79e`. `WEP` calls `ASYMTBKFXEXIT` and `FUN_1010_ca82`.

`BMRDRAWBUTTON`, `BMRDRAWBEVEL`, `BMRDRAWSHADOW1`, `BMRDRAWSHADOW2`, and `BMRDRAWSTATUSBAR` are the drawing. They are button faces and bevels. The init that was stopped does not open a book.

A later stop in the same session was `43EF:2992`, `ASYMCTLPAUSE` (line 3606), not `ASYMCTLPAUSED` (line 3656). The prologue has not run, so `DS` is still `3327`. The watch `3327:1B02 = 5341` is not the word the compare reads. After `mov ds, ax` the compare is `41FF:1B02`, which is `DAT_1020_1b02`. `ASYMCTLPAUSE` calls `FUN_1008_34de` and, on a hit, `UNHOOKWINDOWSHOOKEX`. `ASYMCTLPAUSED` only returns 0 or 1. `ASYMCTLISAPPREGISTERED` at `2ACE` is the same lookup: `push 0`, `push [bp+6]`, `call near 34DE`. `ASYMCTLGETPROPERTY` at `2D40` calls `GETCURRENTTASK` and then that lookup.
