# 3. Runtime

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| R-001 | Known | The intended launch is `TB80RUN` (32-bit) spawning `TB80NET.EXE` with the book on the command line. The seam is that spawn, not an in-process thunk. | module catalog, `TB80RUN` survey |
| R-002 | Known | `TB80RTM.EXE` is the 16-bit shell. It owns `TBKMain`, `TBKClient`, `TBKChildWindow`, `TBKReserved_1`, `SchedulerWndTB80`, and the frame class created with `TB80MAIN`. A lesson click is delivered to `TBKClient`. | SoftICE class list |
| R-003 | Known | `TB80MAIN.EXE` is a 23552-byte 32-bit stub. It calls `TB80RMT CreateRemoteCallServer` and pumps keys. It is not the book engine. Failure text: “TB80MAIN: Loading ActiveX support failed.” | `TB80MAIN` decompile |
| R-004 | Known | `TB80BAS` is the book server (“ToolBook Server DLL”), 606 exports. `CDBINIT` is ordinal 1. `CDBFILEOPEN` is ordinal 8. `CDBVIEWPAGE` is 15. `CDBVIEWBKGND` is 18. `CDBPAINTCLIENT` is ordinal 26. | export table, WV-011 |
| R-005 | Known | `TB80RTM` `WM_PAINT` calls `CLIENTTOPAGE`, then ordinal 26. Shape drawing is in BAS, not in RTM. | `tbwp0018/rtm-paint-path.md` |
| R-006 | Known | `TB80RMT` is not on the path that opens a lesson. The 1.5 `PHYSSIZE` index is not in these 8.1 books. | WV-014 |
| R-007 | Known | `nc81int.dll` exports 47 trainer calls. `IntCheckComm130E` opens a port at 9600 8O1, sends a probe, and returns `0x3D` on match or `0x3C` on failure. Families: 130E, TD2000, 5050, 205E. | `nc81int` exports |
| R-008 | Known | `nc81rec.dll` writes `0x46`-byte session records to `SESSION3.REC`. Exports include `RecStartSession`, `RecCloseSession`, `RecBookmarkSession`, `RecWriteResponse`, `RecReadVariable`. | `nc81rec` exports |
| R-009 | Known | On 2026-10-16 the `TB80RTM` exports were broken before the run, and again after one step once the program was running. Neither pass fired. The run went from start to end. At the end the Assembly window was `0000:0000` and `????`. | that session |
| R-010 | Thought | Those symbols were not bound to the code that executed. "Set too early" does not cover the second pass. Why a break set after one live step still missed is not known. | R-009 |

## 3.1 Process

`tbload.exe` finds the book marker and hands off through a vtable at `FUN_00406a70` (virtual call at `00406aa1`, vtable+4). That vtable is not resolved. **Thought:** that call is the first handoff out of the 32-bit search.

`TB80RUN` does not open the book itself. It starts `TB80NET.EXE`. `TB80NET` is a 16-bit NE executable, not a DLL. It is the network access provider (zlib, `TBKNET3WNDPROC`, `TBK.INI`). It does not parse pages.

`TB80W32.DLL` (about 246 exports) and `TB80W16.DLL` (about 406) are the thunk halves. W16 is also the `DoCmd*` command bus (`DoCmdDraw`, `DoCmdMouseDown`). `TBFILE32.DLL` supplies long filenames to the 16-bit engine. `TB80F32L.dll` is the flat 32-bit entry and the common-dialog hook.

`TB80RTM` is the window. Classes seen live include `SchedulerWndTB80` and `TbkNet3TB80` (the latter owned by `TB80NET`). The lesson click does not arrive on `TBKChildWindow`. Break the `TBKClient` window procedure. `BMSG` does not see that 16-bit queue.

## 3.2 Book server and neighbors

| Module | What it is for | What it is not |
|---|---|---|
| `TB80BAS.DLL` | Objects, properties, painters, twip scale, file open | Not the window |
| `TB80CMP.DLL` | OpenScript compile and expand. Resources `0x77` and `0x78` | Not the page walker |
| `TB80UTL.DLL` | Type-name table, string manager, metrics, heaps | Not the `14 00 00` reader |
| `TB80RCR.DLL` | Linked beside the book server. Exports only partly named | Not classified |
| `TB80ENU1.DLL` / `ENU2` | English strings, 16-bit and 32-bit | Not code that opens a book |
| `TB80BMP.DLL` | DIB, metafile, FX blit. Ordinal 3 is the bitmap reader | Not a picture store |
| `TB80JPG.DLL` | JPEG. Version resource still says `TB60JPG.DLL` | |
| `TB80LNL.DLL` | MCI, wave, MMIO. The notify callback is Lionel | |
| `TB80MM.DLL` | `tbkmmNotify`, `imageNotify`, `mciNotify`, `timerNotify` | Does not classify objects |
| `TB80OLE` / `OCX` / `ACX` / `VBX` | Clipboard, controls, automation | Not on the Logic Families paint path |

`linkDLL` libraries add commands only when a handler links them: `TBDLG`, `TBWIN`, `TBDOS`, `TBREG`, `TBDB3`, `TBPDX`, `TBCBT`. `TBCBT` is the CBT scoring extension. Its segment 7 holds the password cipher. See chapter 7. `TBWIN` is `INIT_TBKWIN` and `TBM_EVALUATE`. Neither `TBWIN` nor `TB80NET` walks page records.

Author binaries `TB80EDT.DLL` and `TB80.EXE` are not in this set. The runtime half of the author contract is visible: BAS exports `CDBEDITBOOK`, `CDBVIEWBOOK`, `CDBISVIEWERINGENERICEDITMODE`, `CDBSENDEDITLEAVETOALL*`, and `TBXAUTHORMODE`. RTM calls `GETAUTHORLOCALIZEDDLL`. That is bookmarked, not solved.

## 3.3 NIDA layer

A system book adds script above the book. A `linkDLL` adds commands. Most of what an author treats as “ToolBook” is one of those two, not a new entry point in BAS.

`tb80r.sbk` is the Asymetrix reader book (Help, Bookmarking, Logging, Path manager, Popup Page Manager). It is not the engine. `tb80hyp.sbk` is hyperlink and help. `tb80anm.sbk` is path animation.

The lesson calls `initializebase`, `initializerecs`, and `initializetest` by name. **Thought.** Those names have not been watched as a call log, and the order in `toolbook.lst` has not been watched live. `version.ini` in the set is `03.001.0006`, dated 04-18-05. `CAILT.DAT` maps course ids to Navy CDs. `9E954` maps to DIE. `STDAPPS.LST` is a short encoded list, not a book.

`nc81int.dll` and `nc81rec.dll` are 32-bit PE. They are not Asymetrix. The trainer probe and the session file are the two behaviors that matter for getting a NIDA lesson to run as a lesson rather than as a picture of a page.

## 3.4 What startup has been watched

WDW on W16, before any book open, hits platform detection, OLE init, and the 32-bit thunk: `GETPLATFORMREF`, `IS32BITENV`, `GETRUNTIMELOCALIZEDDLL`, `ACXINITIALIZETOOLBOOKSUPPORT`, `ACXOLEINITIALIZE`, `LOADLIBRARYEX32W`, `GETPROCADDRESS32W`.

WDW on UTL, after `INITTASK`, hits string and task utilities: `GETSTRMGRSTRING`, plugin init, `TBK.INI` profile reads, metrics, `GHEAPCREATE`. No record walk.

The Unicorn host has not opened a book. Pass 06 asks for `TB80.INI` and exits. See chapter 7.

## 3.5 The RTM export list, and a dead task

Watcom's Functions window for `TB80RTM` is 43 exports. `?CALLPROC32W@@Z` at the top of that window is the decorated `CallProc32W` import. The `K`s are Watcom's size marks, not part of a name.

`EGYPT` is the old window prefix. The frame is `MAINWNDPROC`. The client is `EGYPTCLIENTWNDPROC`, the child is `EGYPTCHILDWNDPROC`, and `EGYPTNOTIFYPROC` takes the notifies. `STATUSBARWNDPROC` is the status bar. `SUBEDITCONTROLPROC` subclasses an edit control. `DDEWNDPROC` is DDE. `XDLLTRANSWINPROC` is a window owned by another DLL.

The shell's own book calls are `ENUMWINSFOROPEN`, `BOOKQUERYSAVE`, `EGCDBSAVEBOOK`, and `HANDLEREMOVESCRIPTPROC`. `EGDYNALINKERRORFUNC` runs when a DLL did not load.

Around that frame the names are the product: ASCII file dialogs, cache-file and CD-ROM save, optimized-save progress, the image store, a palette broadcast, the print dialogs, find and its condition dialog, two ask dialogs whose `PL` stem is still unread, resource pickers, `TOOLNOTIFY`, and the remote pair `XCTOLEREMOTECOMMAND` / `XCTOLEREMOTEGET`.

The 12 October export map gives each name a line in `Toolbook/_decompiles/TB80RTM.EXE.c`. A first pass took every call in the next 400 lines and credited it to the export. That mixed in the next function. The following is only what is inside the export itself.

`EGYPTCLIENTWNDPROC` switches on the message. `0x0F` is paint: `FUN_1070_0be0`, or `GETUPDATERECT`, or `FUN_1060_0dca`, depending on the flags at the window struct `+0x124` and `+0x126`. `0x14` returns 1, so the default background erase does not run. `0x02` calls ordinal 76. `0x07` and `0x08` are focus. `0x100`, `0x101`, and `0x102` are key down, key up, and char. `0x104` and `0x105` return without acting when `DAT_1450_0a41` is set. `0x113` is the timer. `0x4A` is `WM_COPYDATA`. Help ids `0x7DF9`, `0x7E02`, and `0x7E03` go through `CXTHELPSETCONTEXT`.

`MAINWNDPROC` is 57 lines. The message is private: `0x41`, `0x4AA`, `0x4AB`, `0x4D8`, `0x4D9`. `0x111` is `WM_COMMAND`. A fixed set of command ids goes to `FUN_1098_0124`, and the rest to `FUN_1368_0000`.

`BOOKQUERYSAVE` resolves the path with `ASYM_GETLONGFILENAME` when the process is 32-bit. If `DAT_1450_0a41` or `DAT_1450_0a45` is set it returns 7 and does not prompt. Otherwise it prompts through `FUN_1068_0034` with style `0x31`.

`EGCDBSAVEBOOK` is the same shape and it does not call `CDBGETVALUEEX`. An empty name, or either of those two flags, sets the result to 7. Otherwise it prompts with style `0x24` or `0x30` and returns whether the answer was 6.

`HANDLEREMOVESCRIPTPROC` is a dialog procedure. `0x110` sets the item text from ordinal 106. `0x111` with a zero id calls `ENDDIALOG`. `EGDYNALINKERRORFUNC` returns immediately unless the id is `0x1FAC` or the `_C_FILE_INFO_` id, then calls ordinal 161. `POSTPALCHNGTOOTHERS` is seven lines: `SENDMESSAGE` of `0x311`, which is `WM_PALETTECHANGED`, and return 1. `CHANGEPRINTERDIALOGPROC` reads and writes the profile string. `ASCIIFORMATDLGPROC` is a dialog on `0x110` and `0x111`, command ids `1`, `2`, `0x106B`, and `0x106C`. `PLASKDIALOGPROC` and `PLREQUESTDIALOGPROC` end the dialog. The `PL` stem is still not a word in the listing. The palette helpers `TBKPALAPPEND` and `CREATEPALETTE` sit in the next function, not in `POSTPALCHNGTOOTHERS`.
