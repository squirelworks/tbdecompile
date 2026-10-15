# 15. System books and the NIDA shell

`.sbk` and `.tbk` are the same container. Most of the Asymetrix `.sbk` files are resource containers: an object-type name table and menu resources. A few carry compressed handlers. The NIDA lesson still opens if the system books are removed. What breaks is the shell: blue screen, resize, and the menu. Renaming `nida81.tbk` removes the splash and reports that the shell is not a book. The lesson can still be entered.

## 15.1 Type names

The name table, in the order recovered from the system books, is: ComboBox, Stage, Picture, Hotword, RecordField, PaintObject, Curve, AngledLine, Pie, Arc, IrregularPolygon, Polygon, Line, RoundedRectangle, Ellipse, Group, Field, Button, Rectangle, then Page, Background, Book.

In `nc81base.sbk` that table sits around file `0x15E4`–`0x1ADC`. Curve's type id is `0x05C7` at file `0x1810`. The schema spelling `IrregularPloygon` is the 11.5 XSD, not this table.

These names are not yet tied to the kind byte inside a `14 00 00` chunk. `TB80UTL` holds the strings. It has not been shown to be the function that classifies a chunk.

## 15.2 NIDA shell

`nida81.tbk` is a real book. 43 objects. Pages `P20000` through `P22130`. It does not name lesson ids. It has 100 `buttonClick` handlers in the same bytecode as a lesson. P310 is Minimum Requirements (586, 133 MHz, 12 MB RAM, 1 GB, mouse, Windows 98). P20001 is the small menu. P22130 is Test Console Setup.

`9e954d01.tbk` at file `0xB1A96` names `tb80r.sbk`, `nc81trnr.sbk`, `nc81base.sbk`, `nc81recs.sbk`, and `nc81test.sbk`, and it calls `initializebase`, `initializerecs`, `initializetest`, `openSession`, and `gotoPageList`. It also jumps to `nida81.tbk` and to `93954302.tbk`.

**Thought.** Those initialize names have not been watched as a call log, and the order in `toolbook.lst` has not been watched live. `version.ini` in the set is `03.001.0006`, dated 04-18-05. `CAILT.DAT` maps course ids to Navy CDs. `9E954` maps to DIE. `STDAPPS.LST` is a short encoded list, not a book.

## 15.3 Asymetrix `.sbk` tiers

Sizes are the files that were triaged. JBO is at `0xC00` unless noted.

| Tier | File | Size | What it is for |
|---|---|---|---|
| Core | `tb80r.sbk` | 954 KB | Reader book. 66 objects. 33 compressed handlers (chapter 14). Help, bookmarking, logging, path manager, popup page manager. Not the engine. |
| Core | `tb80.sbk` | 3.1 MB | Large core system book. Type table present. Not fully extracted. |
| Core | `tb80a.sbk` | 2.4 MB | Author-side companion. Not on playback. |
| Core | `tb80i.sbk` | 619 KB | Instructor system book. |
| Core | `INST80.SBK` | 70 KB | Installer book. Referenced by Inst80. Names `tb80r`. |
| Useful | `tb80hyp.sbk` | 141 KB | Hyperlink and help. No decoded `to handle` text. |
| Useful | `tb80anm.sbk` | 64 KB | Path animation. No decoded `to handle` text. |
| Useful | `tb80aicc.sbk` | 86 KB | AICC strings. Not shown to be required for a local page. |
| Useful | `tb80actr.sbk` | 208 KB | ActiveX runtime. |
| Parked | `tb80acta.sbk` | 2.1 MB | ActiveX author. |
| Parked | `tb80axf.sbk` | 618 KB | ActiveX related. JBO at `0xE00`. |
| Not on the local path | `tb80web.sbk` | 1.1 MB | Web. |
| Not on the local path | `tb80ftp.sbk` | 243 KB | FTP. JBO at `0xE00`. |
| Not on the local path | `tb80x.sbk` | 256 KB | Unclassified specialty. |
| Not on the local path | `tb80lmx.sbk` | 62 KB | Small. JBO at `0xE00`. |

An early triage said system `.sbk` files do not contain OpenScript. That is superseded for `tb80r.sbk` only. The other rows above still have no decoded handler text.

The four NIDA books `nc81base`, `nc81recs`, `nc81test`, and `nc81trnr` are password-protected resource containers. Runtime opens them without the password. The author path is the one that asks. The password is not required to read this decompile. Chapter 16 is the cipher, not the password.

## 15.4 Trainer and session DLLs

`nc81int.dll` and `nc81rec.dll` are 32-bit PE. They are not Asymetrix.

`nc81int.dll` exports 47 trainer calls. `IntCheckComm130E` opens a port at 9600 8O1, sends a probe, and returns `0x3D` on match or `0x3C` on failure. Families: 130E, TD2000, 5050, 205E.

`nc81rec.dll` writes `0x46`-byte records to `SESSION3.REC`. Exports include `RecStartSession`, `RecCloseSession`, `RecBookmarkSession`, `RecWriteResponse`, `RecReadVariable`. `initializeRecs` on the shell clears responses when a session loads. That last sentence is inferred from the shell script, not from a live trace of the DLL.

## 15.5 `linkDLL` versus a system book

A system book adds script above the book. A `linkDLL` adds commands, and only when a handler links it. The set that shows up that way is `TBDLG`, `TBWIN`, `TBDOS`, `TBREG`, `TBDB3`, `TBPDX`, and `TBCBT`. `TBWIN` is `INIT_TBKWIN` and `TBM_EVALUATE`. Neither `TBWIN` nor `TB80NET` walks page records. `TBCBT` is the CBT scoring extension and the password cipher. It is not the record reader.
