# SoftICE field notes

Closed 11 Oct 2026. This is the SoftICE half. WDW is the Watcom chat. A Debugging chat reads both and does not mix commands.

Selectors below are examples from the boot where they were seen. Copy offsets. Remap selectors.

## 00 How to use this

Confirmed: seen on the VM. Trap: already cost a reboot. Open: not finished. Scaffold: heading is real, steps not re-run.

## 01 Standing orders

- Ctrl+D enters SoftICE. MAP segment numbers are hex. BAS(0A) is segment 10. BAS(21) is segment 33.
- T into a call. P over it. G runs. F12 is P RET and paints the splash on a load.
- BC * before the next breakpoint. A live GDI!POLYGON breakpoint freezes SoftICE if the page scrolls.
- 14 00 00 01 does not become 14 00 00 11. Later live 80 65 objects used 14 00 00 02.
- A dump that is the SoftICE window, or the DOS device chain CON / AUX / PRN, missed.
- Do not search all of memory. The wide 80 65 search found nothing and can GPF the VM.

## 02 Session start

```
BC *
MAP TB80BAS
MAP TB80BMP
MAP TB80RTM
U <sel>:0
BPX <sel>:<offset>
G
```

Invalid selector or invalid address: that guess is not loaded. MAP again, then LDT. Who owns a selector is MAP, not a guess. Stop before the splash if the photograph is the target.

## 03 Stepping

Calls that painted the splash on that boot: CALL 0614 in BMP(7); a short call in BAS(37) near 017F or 01A6; a near call in BAS(2); F12 in that neighborhood. If SoftICE pops on a breakpoint you forgot, BC * and set the new one. Do not stack them.

## 04 Book probe

PUSH CS / CALL 2F00 at BAS 316F:1791. D DS:BX is the path. P over system books. Do not F12.

Names on that loop: NC81BASE.SBK, NC81RECS.SBK, NC81TRNR.SBK, tb80anm.sbk, tb80r.sbk. Splash book is nida81.tbk. Outer frame: 2F2F:183D toward 316F:1766.

The loop is one hit per book, not a bug. The BMP signature check to try next is segment 7 offset 0x805. Identified, not confirmed live. Remap BMP(7). T in.

## 05 Paint stops

One hit, read the object, BC *. Do not scroll with these set.

- GDI!POLYGON. 11 points is one gray pin tip, not the chip. Points at DS:30AC. Object at [BP+04]. Count at +0x30. Pointer at +0x32. 4 bytes each, twips. Paint function BAS 0x82:0x376.
- GDI!POLYLINE. P1170 bracket was 4 computed points. Bounds twips at +0x0E, +0x10, +0x12, +0x14.
- GDI!RECTANGLE. BAS segment 0x83. Bounds at object+0x0F. Chip bodies are the small ones.
- GDI!ARC. BAS segment 0x7B. Type word 0x11 at object−2. Box at +0x0F. Fill 0x808080 at +0x18. Four twip pairs at +0x25, +0x29, +0x2D, +0x31.
- GDI!PIE never fires.

Scale is BAS segment 2 offset 0x1DD: (stored * DS:01A6 + 720) / 1440. At 96, screen = twips/15. The repeated pin twips do not include the per-pin shift.

## 06 Clicks and windows

TB80RTM owns TBKMain, TBKClient, TBKChildWindow, TBKReserved_1, SchedulerWndTB80. A lesson click goes to TBKClient. BMSG does not see that 16-bit queue. One boot the proc was 3EF7:051C, Win16 export prolog. tb80r.sbk is a system book, not the engine. TB80MAIN is a 32-bit stub.

## 07 Dumps

Look: D DS:BX, D sel:off L 10, U sel:off L 10, LDT sel.

Real: page.bin01511 (ASYM_TpID), p400.bin0157 (JBO 03 4A 42 4F 01 00 00 08), dump-001 (Viewer Management, id 0x30), dump-002 (System Info, id 0x21). Those two use property block 14 00 00 02.

Junk: page1–page5 and RTMSTR.BIN (console), booknam1.bin (name slot only), rtm.bin and dump-000.bin (DOS device chain).

ICEDUMP 6.021 loaded after kernel32 and user32 exports were in winice.dat. /option n sets screen-dumper mode 1. A filename without * printed a literal name. Memory-dump recipe is not repeatable. The VM has to be off before the host reads the bins.

GetObject(14) only fires during load. Header seen once at flat 0030:C2EF6322: 00 00 43 01 58 01 44 02 01 08 (323×344, 8 bpp, bmBits null). Do not reuse it.

## 08 Where to break

TB80RTM engine. TB80BAS paint. TB80BMP decode. TB80CMP is OpenScript, not this book. TB80UTL is type names. TB80MM is notifies. TB80W16 is the thunk. KERNEL INITTASK belongs to the Watcom notes.

Load order reconstructed from the 06:57 log, screenshots newest-first, so this list is oldest-first: thunk, TB80W32 / F32L / RMT, OLE, TB80RTM, satellites, TB80R and TB80ANM probes, then TBFILE32, TBWIN, TBCBT, TB80BMP, TB80MM, TB80CMP.

## 09 Traps

F12 on the paint call. Stale selectors 1161, 4156, 501E. Full-memory 80 65 search. 01 and 11 treated as a rewrite. Console or device-chain filed as a page. Polygon breakpoint left on while scrolling. 1791 without D DS:BX. Stepping the call that is the paint. GetObject after the splash is up.

## 10 Open

1. Splash decode, buffer still unpainted.
2. One-shot rectangle painter for the chip body, then BC *.
3. One clean memory dump of an address just displayed, then repeat it.

## 11 Command card

```
BC *
MAP TB80BAS
MAP TB80BMP
U <sel>:<off> L 10
BPX <sel>:<off>
BPX GDI!POLYGON
D DS:BX
D DS:30AC
T
P
G
LDT <sel>
```

Not on the card: F12, a full-memory search, old addresses, WDW keys.
