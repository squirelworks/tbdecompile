# Bochs debugging rig: Windows 98 SE + ToolBook 8.0 (TB80BAS.DLL)

## What's installed
- **Bochs 3.0**, built from source (`bochs-3.0.tar.gz` from SourceForge, sha256 `cb6f542b…81aa`) and installed in **/opt/bochs**
  (`/opt/bochs/bin/bochs`, `bximage`, BIOS/VGABIOS in `/opt/bochs/share/bochs`).
  configure flags: `--enable-debugger --enable-x86-debugger --enable-cpu-level=6 --enable-x86-64 --enable-pci
  --enable-clgd54xx --enable-voodoo --enable-sb16 --enable-es1370 --enable-ne2000 --enable-usb --enable-show-ips
  --enable-iodebug --enable-a20-pin --enable-all-optimizations --with-nogui --with-term --with-sdl2 --with-x11 --with-rfb`
  (configure ignores `--enable-disasm`/`--enable-pnp` in 3.0. The disassembler is built in with the debugger.)
- Debian's packaged `bochs` 3.0 (`/usr/bin/bochs`) is also installed but **has no debugger**. Always use `/opt/bochs/bin/bochs`.
- qemu-utils (qemu-img 10.0), mtools, nasm, plus a Python venv at `venv/` (Pillow, vncdotool).

## Bochs 3.0 gotcha
The debugger only starts when you pass **`-dbg`**. `-rc file` on its own does nothing, and the guest just runs.
`run_debug.sh` always passes `-q -dbg -f … -rc … -dbglog …`.

## Files
| path | what |
|---|---|
| `bochsrc.win98.txt` | Win98SE config: p2_klamath, 128 MB, i440fx, Cirrus 5446, undoable disk, RFB display, magic_break |
| `win98.img` | the user's image (chmod 444). **Never written**: all guest writes go to `win98.redolog` |
| `win98.redolog` | the undoable journal. Delete it to roll back to the pristine image. |
| `run_debug.sh RC [cfg] [timeout]` | runs the debugger with an rc script and writes `logs/dbg_<rc>_<timestamp>.txt` and `.dbglog` |
| `tb80_example.rc` | template rc for ToolBook breakpoints |
| `tools/bochs_driver.py` | starts Bochs with piped stdin/stdout, can break in with SIGINT and run commands periodically |
| `tools/attach_console.py` | sends commands to an already-running driver-started Bochs (via /proc fds). Untested on the live session. |
| `tools/rfbshot.py` | grabs a PNG from the Bochs RFB display (port 5901, 8bpp, so colours are approximate) |
| `tools/rfbkey.py` | sends keys to the guest (`Return`, `Escape`, `alt+s`, …) |
| `tools/memsearch.py` | byte-signature search (with `??` wildcards) in a `writemem` dump |
| `tools/ne_info.py` | NE parser: segment table and exports, mapping export → NE seg:off → Ghidra address |
| `extracted/` | TB80BAS/UTL/W16/RTM copied out of the image (read-only mtools) |
| `full_listing.txt` | recursive directory listing of C: |
| `test/` | floppy boot-sector tests proving lb/vb/magic-break/r/sreg/u/x/info gdt/info ldt/writemem work |

## Disk geometry
The image is 2,096,898,048 bytes, which is 4,095,504 sectors and exactly **4063 cyl × 16 heads × 63 spt**.
The MBR partition (type 0x0B, LBA 63) ends at CHS 1014/63/63, and the FAT32 BPB says 64 heads / 63 spt.
That is the BIOS LARGE-translated view of 4063/16/63, so the config uses `cylinders=4063, heads=16, spt=63, translation=large`.
The Bochs log confirms `PCHS=4063/16/63 translation=large LCHS=1015/64/63`, and the guest boots.

Other image types: Bochs reads fixed and dynamic VHD directly (`mode=vpc`). Differencing VHDs (86Box child images) and
.hdi/.hdx must be converted first: `qemu-img convert -O raw parent_or_child.vhd win98.img` (qemu follows the parent chain).

## Running
- **Debugging a fresh boot:** `./run_debug.sh myscript.rc`. The rc script's first command runs at the reset vector. End it with `q`.
- **Watching the screen:** `venv/bin/python tools/rfbshot.py shots/now.png`. Keys go through `tools/rfbkey.py`.
- Bochs locks the redolog, so only one Bochs can use this config at a time.
- Ctrl-C (SIGINT) breaks into the debugger. `c` continues.

## Win16 address mapping (important)
1. **Ghidra segment → NE segment number.** Ghidra's NE loader numbers segments `0x1000 + (n-1)*8`.
   This was verified against the DLL's entry table: `OBJFILEOPEN` is NE **47**:177c, which is Ghidra 1170:177c,
   and `OBJLOCK` is 47:0308, which is Ghidra 1170:0308. This matches the decompile.
   `CDBFILEOPEN` is 10:017a (Ghidra 1048:017a), the same segment as reader `FUN_1048_1766`, and `CDBPAINTCLIENT` is 3:0506 (Ghidra 1010:0506).
   Run `python3 tools/ne_info.py extracted/TBK/TB80BAS.DLL [NAME…]` for the rest.
2. **NE segment → runtime selector.** This is assigned by KERNEL at load time and differs on every boot.
   Under Win98, Win16 code selectors are LDT selectors with TI=1 and RPL=3, so the low 3 bits are 7 (e.g. `0x1a7f`).
   CS is the selector, and the linear address is the LDT descriptor base + offset (`info ldt <sel>>3>`).
   `vb sel:off` matches the **exact** CS value (tested: a breakpoint on 0x000f did not fire when CS was 0x000c).
   `x /Nbx sel:off` and `u /N sel:off` accept selector:offset (tested).
   `lb` takes a linear address. That is fragile for moveable or discardable segments, which can move or be discarded and reloaded.
3. **Ways to find the selector** once TB80RTM has loaded TB80BAS:
   - In the guest, use WDW, or another tool that lists module segments (TOOLHELP `ModuleFindName` / `GlobalEntryModule`) to read seg 47's selector directly.
   - Search memory: `writemem "/workspace/bochs/dumps/lin.bin" 0x80000000 0x1000000` (or another linear range),
     then `tools/memsearch.py dumps/lin.bin "<bytes>"`.
     Look for the in-memory NE header of module `TB80BAS`: "NE" followed by the resident name `TB80BAS`. Its in-memory segment table
     has a handle for each segment, and the selector is derived from it (check with `info ldt`).
     Or search for the runtime bytes of a function you know, then use `info ldt` to find which selector's base covers the hit.
   - **Byte signatures from the DLL file don't work for TB80BAS.** Its code segments are compressed on disk
     (segment flag 0x0008, entropy about 7.8 bits/byte). The bytes at file offset seg47+0x177c are not x86 code.
     Also, `mov ax,0x2977` in the Ghidra output is the DGROUP fixup value that Ghidra assigned. On disk the immediate is a relocation.
     At runtime it becomes `B8 <DGROUP selector> C8 …`, so search for `b8 ?? ?? c8` with wildcards.
     Only 106 `B8 xx xx C8` sequences exist in the raw file, and those are only incidental matches in the compressed data.
   - `magic_break: enabled=1` means a guest `xchg bx,bx` (bytes `87 db`) traps into the debugger.
     You can `setpmem` it over a function entry after load, but you have to restore the bytes yourself.

## Status at hand-off
See the report from the agent. Bochs was booted from this config with the driver frozen, and it was left running at the Win98 desktop.

## Saved machine state (skip the cold boot)
- `state-reader-p310/` = Bochs save-state taken 2026-10-21 22:19 JST: Win98 desktop, ToolBook **Instructor** (Inst80.exe)
  with C:\TBK\9e954d01.tbk open at **Reader level** on page **P310** ("IBM PC Compatible Computer" picture). No breakpoints set.
- Saved via the RFB header "suspend"/save button (x≈592,y≈15 — click coords use guest_xres 640, not the 720-px RFB width);
  the path prompt appears in the RFB console and ignores Shift (hence the dash/lowercase dir name). Answer `y` to keep running.
- Bochs 3.0 bug: the saved `config` had a malformed `panic:` line (`?=fatal` entries); replaced with `panic: action=ask`
  (original in `config.orig`). Without that fix `bochs -r` aborts.
- Restore: `./restore_snapshot.sh` (stop the running Bochs first). Restore copies the snapshot's redolog over win98.redolog
  (current one backed up to logs/). Verified 22:21 with an isolated copy (state_test/, journal → test/restore_test.redolog,
  RFB port 5903): came up on P310 at Reader level, clock running (shots/restore_test_2.png).
- Win16 selector = module-DB segment-table handle | 1 (verified for TB80BMP and TB80BAS).

## Erase rectangles
Session 2026-10-24 22:2x JST (restore of state-reader-p310, book 9e954d01.tbk reopened, walked to P400 with Alt+Right).
- Hook: `vb 0x2947:0xee0` = FUN_1018_0ee0 (TB80BAS NE seg 4, off 0xEE0; args at stack words 1-4 at entry = left, top, right, bottom). The selector is session-specific: the old 0x2BAF is wrong after the book is closed and reopened. Re-derived from `info ldt` (only code segment with limit 0x1b5f = seg 4 alloc 0x1b50: ldt[0x528], base 0x81611280); bytes at 0x2947:0xee0 = `55 8b ec 83 3e 32 17 00` (push bp; mov bp,sp; cmp word [0x1732],0 = the region handle test in the decompile).
- Reader level (shots/q7.png, P400): one Alt+Right: no page change, no hit (shots/e1.png). The Reader level has no menu bar, so the Go shortcut does nothing; Tab also did nothing (shots/e2.png).
- Author level (F3 off Reader; menu bar and toolbars on screen; shots/e3.png = P400, clock 12:16 PM): one Alt+Right, the page changed to P410 (shots/e4.png, clock 12:18 PM), but the breakpoint at 0x2947:0xee0 was NOT hit during the page change (hitloop waited 20 s: logs/erase_author_p400_p410.out says "no hit within 20.0s"). LDT entry and bytes were still intact afterwards.
- Result: NO erase rectangles recorded for P400 -> P410 through FUN_1018_0ee0. The earlier hits of this function (594,414)-(624,442) came from the Next button's own invert on a mouse click; a keyboard page change does not go through it.

## Mouse capture over RFB (tested 2026-10-24 ~22:23 JST, pid 381754, P410 Author level)
- `tools/rfbcapture.py toggle`: Ctrl keydown (0xffe3), pointer event mask 2 (middle) at (300,300), release, Ctrl keyup. After it the guest arrow cursor jumped from about (122,70) to a box with top-left (421,372) (shots/m0.png -> m1.png): the first absolute RFB position is turned into a relative delta of about (+300,+300).
- Then `tools/rfbcapture.py move 60 40` (10 small absolute steps from (300,300) to (360,340)): cursor box top-left (421,372) -> (481,392) = +60,+20 (shots/m1.png -> m3.png; m2.png is an incomplete all-black RFB frame, ignore). X moved as asked, Y moved +20 of the asked +40 (cause not checked, maybe guest pointer acceleration or rounding).
- So the guest mouse works once capture is engaged with Ctrl+middle. Not engaged after a restore in earlier sessions (pointer never moved). I have not tested whether it survives a restore; capture is a host GUI state, so assume it must be re-engaged after every restore.

### Erase rectangles: Reader level P410, click on Next (Fred, Oct 24 PM)
- Reader level confirmed on P410 (pixel signature (72,72,170) ~94k, (72,0,0) ~76k; clock 12:26 PM).
- Breakpoint: `vb 0x293f:0x16de` = FUN_1020_16de (TB80BAS seg 5; the 0x293f/ldt[0x527] selector re-derived from `info ldt`; bytes `enter 0x1c,0` + `callf 2947:1ab0` match the decompile; the other limit-0x1c5f code segment ldt[0x5a1] is not it).
- ONE hit while the pointer was on / pressing the Next button (hit #1). Entry stack (low address first): `0072 293f | 0e4a 0fe4 0014 0eaf 43d0 ab8e` = ret 293f:0072 (inside FUN_1020_0000), param_11 (status ptr) 0e4a, param_8 (layer/page obj) 0fe4, far ptr to DAT_1630_01f2 = 0014:0eaf, region handle 43d0 (FUN_1018_0ec6 -> record+8), hdc ab8e. Regs at hit: ax 0fe4 bx 24684 cx 0 dx 2f1f ds=es 2f1f ss 3d17 sp aa28.
- So the erase is a FILLRGN of a layer HRGN (screen path), not a rectangle. Rectangle must come from GetRgnBox on 0x43d0 or from screenshot diff. FUN_1018_0ee0 (SetRectRgn) is not on this path for the keyboard change either.
- Blocker: after that hit the page stayed P410; later left clicks (several, held 0.2-1.5 s, also with a 3px nudge) produced no hit and no page change; the pointer vanished for a while and returned after one Ctrl+middle toggle (before c0/after c1 shots show the pointer at ~(604,338)). Capture toggles flip state each time; I toggled an even/odd number of times, so check the pointer before assuming state. Breakpoint cleared (blist empty), Bochs left running, no snapshot.
- Tools added: tools/findcursor.py (template match of the guest pointer), tools/mvcur.sh DX DY, tools/rfbclick.py, tools/rfbbtn.py down|up; rfbcapture.py `move` now tracks the pointer in logs/lastptr.txt. Pointer motion is non-linear (x gain ~0.5-1, y gain 0.3-1), so always re-measure.

### Erase rectangles: AUTHOR level, P410 -> P420 by one Alt+Right (Fred, Oct 24 23:01 JST)
- Before: shots/a1.png (P410, Author, "ToolBook II - 9e954d01.tbk", guest clock 12:51 PM). After: shots/a2.png (P420, Author, 12:54 PM; text starts "Apply... volts to one IC might be normal. Applying the same 10 vo... different IC can cause damage.", flame bitmap over right chip).
- Breakpoint `vb 0x293f:0x16de` (FUN_1020_16de): **4 hits** in about 22 s (23:01:50, :57, 23:02:05, :12), then none for 90 s. Log: logs/erase_author_p410_p420.log.
- Every hit: stack `0072 293f | 0e4a 0fe4 0014 0eaf 43d0 <w>` -> caller FUN_1020_0000 (293f:0072), param_11 0e4a, param_8 0fe4, far ptr 0014:0eaf, region handle **43d0 (same on all 4 hits)**, first word <w> = aaae, ac94, ab1c, a9a4 (changes each hit; looks like a stack/pointer value, not a handle, so I do not call it an hdc). Regs constant: ax 0fe4 bx 24684 ds=es 2f1f ss 3d17; rdx/rcx differ on hits 3-4.
- GetRgnBox hook NOT done: on this screen path FILLRGN is used, GETRGNBOX is only on the printer path. Bounding boxes below are screenshot diffs (RFB coords; subtract 40 for guest y; subtract nothing for x), clusters after 6px dilation, a1 vs a2, y 40..484 only:
  - x38..43 y143..152, 32 px (page label P410 -> P420)
  - x75..114 y221..254, 422 px and x176..552 y221..254, 2988 px (the two text lines; only glyph pixels differ, field background pixels are identical)
  - x366..490 y319..376, 3845 px (flame bitmap)
  - x234..442 y359..483, 953 px (the thin white line and the lower pin row)
- Reader level vs Author level not compared in this run (Reader click was blocked).
- Bochs left paused, breakpoint cleared (blist empty). No snapshot. Start-button test not done.

## Erase rectangles: ablation of FUN_1020_16de, P420 -> P430 by Alt+Right, Author level (Fred, Oct 24 ~23:50-00:10 JST)

Method: bp `vb 0x293f:0x16de`; at hit K read rsp, `set esp=rsp+16; set eip=0x72; set eax=1` (a retf of the 12 argument bytes with AX=1 so FUN_1020_0000 carries on, the fill is not executed). Screenshots only possible at the guest running (RFB does not answer while the debugger prompt is active; paused and just-after-continue shots failed 5 of 5 times), so per-hit boxes can't be read from per-hit screenshots; the ablation compares whole-page results instead.

| run | hits skipped | hits seen | result screenshot | diff vs normal P430 (`sk_post0.png`) |
|---|---|---|---|---|
| baseline | none | 5 | `shots/sk_pre0.png` (P420) -> `shots/sk_post0.png` (P430, 1:?? PM) | - |
| k1 | hit 1 only | 5 | `shots/k1_post.png` (P430, 1:19 PM) | 0 changed pixels (>30 level) |
| k4 | hits 1,2,3,4,5 (all) | 5 | `shots/k4_post.png` (P430, 1:28 PM) | 0 changed pixels (>30 level) |

Pre-state for k4: `shots/k3_back.png` (P420, 1:24 PM, flame bitmap over the right chip).
Region handle passed to every call: 43d0 (same on all hits, both runs). Stack pointers at hit 1..5 in the k4 run: cbaea948, cbaeab2e, cbaeaa1a, cbaea9b6, cbaea83e.
Conclusion: with all five FILLRGN calls of FUN_1020_16de removed, the P420 flame is still erased and P430 is pixel-identical, so on this transition 16de is not what erases the flame. Caveat: no positive control yet (a case where skipping does change the screen).

## Colour calibration (Fred, from `shots/k4_post.png`, P430, 1:28 PM)
Windows navy title bar region (200..500, y 42..54): (72,0,0) on all 3600 px. Taskbar (330..540, y 488..520): (218,218,170) for 5040 px, white 1595. Toolbar/menu grey: (218,218,170). No 16-colour desktop colour is visible (window is maximised). So Windows' navy (0,0,128) shows as (72,0,0) and silver (192,192,192) as (218,218,170): the RFB palette is not trustworthy for hue; only black and white are right. Red/blue in the page are therefore swapped/shifted by an unknown mapping.

## Step 2: region bounding boxes at each FUN_1020_16de hit, P420 -> P430 by Alt+Right, Author level (Fred, Oct 24 ~00:20 JST)
CORRECTION to the earlier "region handle 43d0 on all hits": at entry of 293f:16de the stack (low first) is `ret IP 0072, CS 293f, param_1, param_2, far-ptr offset, far-ptr segment, param_4, param_5`. 43d0 is param_4. The region passed to FillRgn is param_2 (the code pushes [bp+6]=hDC, [bp+8]=hRgn, brush at obj+0x49, to the GDI FillRgn wrapper at 0507:0000, which type-checks it as 0x4f4c via the handle table). Region handle = param_2 = 0fe4 (hit 1) and 0fd8 (hits 2-5), so NOT the same handle on all hits (hDC param_1 = 0e4a hit 1, 0e22 hits 2-5).
How read: GDI heap selector 0x05af = ldt[0xb5], base 0x81cd3000. Handle table dword at heap+0x10000+handle gives the object offset (0fe4 -> 0x27864, 0fd8 -> 0x27ad4). Object words (hex, from object start): w1 = 4f4c (type), w11..w14 = left, top, right, bottom, then a scanline-like block `2, top, bottom, left, right`. Decode checked only by this self-consistency (bbox words equal the scanline words); GetRgnBox is not on the screen path so no cross-check by call.
| hit | param_1 (hDC) | region handle | object offset | bbox l,t,r,b (decimal) | words w11..w14 |
|---|---|---|---|---|---|
| 1 | 0e4a | 0fe4 | 0x27864 | 24,24,604,182 | 0018 0018 025c 00b6 |
| 2 | 0e22 | 0fd8 | 0x27ad4 | 0,0,624,442 | 0000 0000 0270 01ba |
| 3 | 0e22 | 0fd8 | 0x27ad4 | 0,2,86,23 | 0000 0002 0056 0017 |
| 4 | 0e22 | 0fd8 | 0x27ad4 | 0,0,624,442 | 0000 0000 0270 01ba |
| 5 | 0e22 | 0fd8 | 0x27ad4 | 24,24,604,182 | 0018 0018 025c 00b6 |
Far pointer (layer object) param_3: 0d97:0014 on hit 1, 0eb7:0014 on hits 2-5. Raw dumps: logs/rgnbox_hits.log; tool tools/rgnbox.sh. Pre-state screenshot for this run: shots/n1.png (P420, 1:30 PM). Region coordinates are in the DC's coordinate space (unknown origin); no erase rule is drawn from this.
Breakpoint cleared; Bochs left paused at the prompt (stopped inside the 5th hit of FUN_1020_16de, guest page still P420->P430 in progress).

## Step 3: known-colour shot (Fred, Oct 24 ~00:35 JST)
shots/p400b.png copied to /tmp before reading: title "ToolBook II - 9e954d01.tbk", corner label P400, guest clock 1:39 PM, Author level. File says P400 background is solid (0,0,191). Pixel values actually in the screenshot file, background areas outside the page objects: see the numbers reported to Frank; they are (72,0,0) and (109,0,0), not (0,0,191). Together with the title bar (72,0,0) for Windows navy (0,0,128), the screen palette is not a faithful colour mapping. Colour closed as evidence.

## Step 4: Reader-level page shots (Fred, Oct 25 ~00:00 JST)
Route: Author level, Go > Previous/Next Page (Alt+Left/Alt+Right; the Go menu has First/Last/Back/History but no go-to-page), F3 to Reader for the shot, F3 back. Page order in 9e954d01.tbk (from the reader's page list): P0, P1, P10, P100, P300, P400, P410 ... P450, P900.
- P300: shots/r300.png, title "Nida Corporation - Logic Families", corner label P300, clock 1:44 PM.
- P1: shots/r1.png, title "Nida Corporation - Logic Families", corner label NOT VISIBLE (cannot read); content is the "LESSON INFO" page whose Filename/Title/Revision Date fields are on layer P1 in the file; 3 Alt+Left presses from P300. Clock 1:48 PM.
- P450: shots/r450.png, title "Nida Corporation - Logic Families", corner label P450, clock 1:52 PM (Author shot shots/a450.png, label P450, 1:52 PM).
- P900: NOT TAKEN. Bochs process (pid 381754) disappeared at about 00:02 JST, right after the F3 back to Reader at P450; no error in the console log (last lines are the blist output), RFB refused connections. Parked per instructions; no restart, no restore.
## Install listing
Static, from the image listing: tbk_files_by_folder.txt (names, sizes, folders). C:\TBK holds 9e954d01.tbk, nida81.tbk, nc81bank.sbk, nc81base.sbk (67938), nc81recs.sbk, nc81test.sbk, nc81trnr.sbk. System books in Program Files/Common Files/click2learn/TBSystem (tb80r.sbk 953705, tb80actr, tb80anm, tb80ftp, tb80hyp, tb80aicc) and Program Files/click2learn/Instructor8 (tb80.sbk 3086352, tb80a.sbk, tb80i.sbk, tb80web.sbk, tb80x.sbk, tb80axf.sbk, tb80acta.sbk, tb80lmx.sbk, inst80.sbk).

## P900 shot + Bochs restart (Fred, Oct 25 ~00:55 guest / 00:15 JST)
Bochs had died (no error). Restart: stale `win98.redolog.lock` removed, then `restore_snapshot.sh state-reader-p310` (new pid 493609, RFB 5901; the script's own `c` came too early, sent `c` by hand). Guest came up on nida81 P310 (clock 11:45 AM). F3 to Author, Ctrl+O, typed `9e954d01.tbk` in C:\TBK, opened at P1; 10 x Alt+Right to P900 (checked at P450 then P900 in Author level, shots/a900.png, shots/a900b.png), then F3 to Reader.
- P900: shots/r900.png (copied to /tmp before reading): title "Nida Corporation - Logic Families", corner label P900, clock 12:54 PM. Page shows LESSON MENU with "1. TTL Integrated Circuits", "2. Other Integrated Circuits", "3. Final Quiz", "* Lesson Exit". Nothing clicked on the page.
Bochs is running (not paused), Reader level, on P900 of 9e954d01.tbk. This guest is a restore of the p310 snapshot plus later actions, so its 9e954d01 session is new.

## P900 click test (Fred, Oct 25 ~00:20 JST; guest clock 12:54-12:57 PM)
Mouse capture was OFF after the restore; `rfbcapture.py toggle` turned it on. rfbmouse.py args are about 2x the guest pixels here (args 600 680 put the arrow tip at guest (302,338)).
(1) Click on empty pink at guest (~302,338), below "Lesson Exit": shots/c3.png (copied to /tmp before reading): title "Nida Corporation - Logic Families", corner label P900, clock 12:55 PM. No change.
(2) Hover on "* Lesson Exit": button face turns white (shots/c4.png, 12:56 PM). Click: shots/c5.png, 12:56 PM, still P900, modal dialog with text "Are you sure you want to Exit the Lesson?" and buttons "Yes" and "No" (title bar of the dialog: cannot read, it is dark with no legible text). Answered No (click on No): shots/c7.png, 12:57 PM, title "Nida Corporation - Logic Families", corner label P900, dialog gone, Lesson Exit still highlighted white (hover). Other three buttons not clicked. Capture is ON, Bochs running.

## P450 click tests (Fred, Oct 25 ~00:30 JST; guest clock 12:58-1:02 PM)
Route: from P900 Reader, F3 (Author), Alt+Left (P450, shots/n450a.png, 12:58 PM), F3 (Reader). On P450 both buttons are mostly off the bottom of the 640x480 screen (page rect bottom 6630 twips; Windows taskbar covers it); only a strip of about 7 px shows at guest y ~437-444 (RFB y ~477-484). Clicked in that strip with the cursor tip verified in a zoom first. rfbmouse.py args: X 1190, Y 892 for Menu (right, RFB ~596,479); X 48, Y 894 for Back (left, RFB ~24,479).
(1) Menu click: shots/m2.png (copied to /tmp before reading): title "Nida Corporation - Logic Families", corner label P900, clock 1:00 PM, LESSON MENU with four labels. 
(2) Back (after returning to P450 via F3, Alt+Left, F3; shots/n450b.png 1:01 PM, m3.png Reader P450 1:01 PM): shots/m4.png: title the same, corner label P440, clock 1:02 PM, text "ICs are classified into logic families based on voltage requirements, speed and the number of circuits they can drive." with houses TTL, CMOS, ECL, IIL.
Nothing else clicked. Bochs running, Reader level, on P440.

## P900 menu click tests (Fred, Oct 25 ~00:40 JST; guest clock 1:03-1:08 PM)
Route to P900 from P440: F3 (Author), Alt+Right x2, F3. Back to P900 after each landing: F3, then Alt+Left (from P1001) or Shift+F2 Back (from P2001), F3. Buttons: hover turns the face white; rfbmouse.py args X 640, Y 210 / 316 / 424 (RFB y 145 / 198 / 252). Nothing clicked on landing pages.
(1) "1. TTL Integrated Circuits": shots/q1.png, title "Nida Corporation - Logic Families", corner label P1001, clock 1:04 PM, heading "TTL INTEGRATED CIRCUITS", buttons "- Discussion" and "- Summary".
(2) "2. Other Integrated Circuits": shots/q3.png, corner label P2001, clock 1:06 PM, heading "OTHER INTEGRATED CIRCUITS", buttons "- Discussion" and "- Summary".
(3) "3. Final Quiz": shots/q5.png, corner label P10004, clock 1:08 PM, heading "FINAL QUIZ", buttons "- Begin" and "- Directions".
No dialogs appeared. Bochs running, Reader level, on P10004, capture ON.

## P400 / P300 click tests (Fred, Oct 25 ~00:55 JST; guest clock 1:11-1:15 PM)
Route to P400 from P10004: F3 (Author), Alt+Up (P0), Alt+Right x5 (P400, shots/n400a.png 1:11 PM), F3. Nav strip clicks: Next at rfbmouse.py args 1232 892 (RFB ~616,479; Next rect x 8907..9342), Back at 48 894; cursor tip checked in a zoom before each click. Title on P300/P400/P410: "Nida Corporation - Logic Families".
(1) P400 Next: shots/t1.png, corner label P410, clock 1:12 PM, text "But, are all ICs the same? Do they all operate on the same voltages?".
(2) P410 Back: shots/t2.png, corner label P400, clock 1:13 PM (heading INTRODUCTION).
(3) P400 Back: shots/t3.png, corner label P300, clock 1:14 PM (heading EQUIPMENT REQUIRED, bar "1. IBM PC Compatible Computer").
(4) P300 bar "1. IBM PC Compatible Computer" (hover turned it white first, shots/t3h.png): shots/t4.png, title "ToolBook II - nida81.tbk", corner label P310, clock 1:15 PM, heading "IBM PC Compatible Computer", Minimum Requirements list. Nothing clicked on the landing page. Not stuck: Reader level, now in nida81.tbk P310, capture ON, Bochs running.

## Empty-page clicks (Fred, Oct 25 ~01:05 JST; guest clock 1:16-1:25 PM)
Return to 9e954d01 from nida81 P310: F3 (Author), Ctrl+O, typed 9e954d01.tbk (dialog in C:\Tbk), Return; nida81 closed, 9e954d01 opened at P1 (Author), F3 for Reader. Title on all 9e954d01 pages: "Nida Corporation - Logic Families". Empty spots were pink/dark red areas with no button; the pointer was shown in the "before" shot each time.
- P1 (LESSON INFO; corner label cannot be read on P1, page identified by its content, shots/e_p1.png 1:17 PM): click at RFB ~(482,280), the pink area right of the text: shots/e1.png, corner label P10, clock 1:18 PM, page "LESSON TITLE" ("Hello Student, this lesson is about: LOGIC FAMILIES"). So the click went to the next page.
- P300 (shots/e3h.png 1:19 PM before): click at ~(320,330): shots/e3.png, corner label P300, 1:20 PM, no change.
- P400 (shots/e4h.png 1:21 PM before): click at ~(320,430): shots/e4.png, P400, 1:22 PM, no change.
- P450 (shots/e5h.png 1:24 PM before): click at ~(320,330): shots/e5.png, P450, 1:25 PM, no change.
Route P10 to P300: Alt+Right x2; P300 to P400: x1; P400 to P450: x5, each in Author level with F3 either side. Bochs running, Reader level on P450, capture ON.

## P400 body field properties (Fred, Oct 25 ~01:20 JST; guest clock 1:28-1:32 PM)
Route: from P450 Reader, F3 (Author), Alt+Left x5 to P400 (shots/f0.png 1:28 PM). One click (no motion) on the body text at RFB ~(300,235) selected the field (handles shown, shots/f1.png). Alt+O showed the Object menu (shots/f2.png 1:29 PM: "Properties for Text Field... Shift+F6", also Page/Background/Book/Lesson; "Extended Properties... Ctrl+F6" greyed). Escape twice, then Shift+F6 opened the non-modal palette "Properties for Text Field" (Name "Text", Layer 1 of 13, ID 9); tabs read with Ctrl+Tab, nothing typed or changed.
- Draw (shots/f3c.png, 1:30 PM): Border style "Inset"; Field type "Word wrap"; Draw transparent off; Draw baselines off; Visible on; Use custom colors (fill blue, stroke white); no border width control on this tab.
- Bounds (shots/f4.png, 1:30 PM), page units: Left 600, Top 600, Width 8205, Height 1890.
- Font (shots/f5.png, 1:30 PM): Font Arial, Font style Bold, Size 12; Underline off, Strikeout off, Normal (no super/subscript).
- Paragraph (shots/f6.png, 1:30 PM), page units: Alignment left; Line spacing single; Indents First line 360, Other lines 360, From right 310; Tabs Spacing 720, Type left.
- Behavior (shots/f7.png, 1:31 PM): tooltip empty; Enable the field on; Typing: "Lock the text and activate mouse events if the field is enabled".
Closed with the palette's Close button (tooltip "Close", Escape did not close it); no OK/Apply exists. Field left selected, book unchanged, not saved. Bochs running, Author level, P400.

## Four-field read (Author level, 9e954d01.tbk, Properties palette; read-only, nothing typed/saved)
Dialog title "Properties for Text Field"/"Properties for Group", window title "ToolBook II - 9e954d01.tbk", clock 1:35-1:50 PM. Shots shots/g_{p450,p900g,p1f,p1t,p1c,p300g}_{0..5}.png (copied before reading). Twips.
- P450 sentence: Name "text", Layer 1 of 3, ID 2. Bounds 600/600/8205/1890 (L/T/W/H). Arial Bold 12. Left, single, indents 360/360(other)/310(right), tab 720 left. Border Inset, Word wrap, locked text + mouse events.
- P900 "1. TTL Integrated Circuits": a click selects GROUP "Selection 1" (Layer 5 of 8, ID 20), bounds 2536/975/4320/600, Font name Arial, style Bold, size box blank, indents 0/0/0, tab 720, line style None, draw transparent, "Make radio buttons mutually exclusive" ON. Ctrl+click, Ctrl+click and Alt+click did not reach a member; not ungrouped.
- P1 Filename line: Text Field "Filename", Layer 4 of 11, ID 18. Bounds 1950/1140/5265/285. Arial Bold 12, left, single, indents 0/0/0, tab 720. Border None, Word wrap, draw transparent, locked.
- P1 Title: Text Field "Title" (own field, also covers the empty line below), Layer 8 of 11, ID 22. Bounds 1950/1440/5775/585. Arial Bold 12, left, single, first line 0, other lines 650, right 0, tab 720. Border None, Word wrap, transparent, locked.
- P1 Copyright: Text Field "Copyright", Layer 2 of 11, ID 9. Bounds 248/4500/9390/1800. Arial Bold 10, left, single, indents 720/720/720, tab 720. Border None, Word wrap, draw transparent, custom colors (fill reddish, stroke black), locked.
- P300 "1. IBM PC Compatible Computer": click selects GROUP "Selection1", Layer 3 of 5, ID 18, bounds 1762/1170/5925/570, Font name box blank, style Bold, size blank (mixed), indents 0/0/0, tab 720, line style None, transparent, radio-exclusive ON.

## P1310 quiz order: Bochs died, parked (Fred, Oct 25 ~01:25 JST)
From P300 (Author, 1:50 PM) Go menu has no go-to-page; 7 x Alt+Right spaced 7 s reached P900 (shots/k_n1.png, 1:53 PM; spacing 7 s is enough). P1310 is page #53 vs P300 #5 (48 presses). During the next batch the Bochs process vanished (no bochs process, RFB 5901 refused on every key, no error in console log). Parked as ordered: no restart, no restore. Restart recipe is in the section above (restore_snapshot.sh state-reader-p310, remove stale win98.redolog.lock, send c by hand, Ctrl+O 9e954d01.tbk).

## P1310 quiz read (Fred, Oct 25 ~01:55 JST; guest clock 12:38-12:49 PM)
Restart: removed stale lock, restore_snapshot.sh state-reader-p310 (pid 604854), sent c by hand, F3, Ctrl+O, typed 9e954d01.tbk Return -> P1. Go menu has no go-to-page (Alt+G: Next/Previous/First/Last/Back/History only); did not try Ctrl+G (Ungroup). Alt+Right x ~51 in batches of 10-12 spaced 7 s, label shots every ~10 pages (P410, P1070, P1170, P1250, P1310 at 12:45 PM); no crash this time. After F3: shots/k_p1310_reader.png (title "Nida Corporation - Logic Families", corner P1310, 12:46 PM).
- P1310 Reader: question text "If an IC has a fan-out of 10 and a fan-in of 1, how many ICs can it drive?" in a cream panel; three orange buttons labelled "1", "10", "11" at left (no letters, no OK, no visible "correct" text); an IC picture at right. Nothing else drawn.
- Click "10" (shots/k_after10.png, 12:47 PM): corner P1311, same question page, button "10" now light cyan, banner "CORRECT!" (top part only; rest hidden under the taskbar) at the bottom. 
- Reader: Alt+Left does nothing; Shift+F2 raises "Are you sure you want to Exit the Lesson?" (answered N). Back button strip (args 48 894) returned to P1310.
- Click "1" (shots/k_wrong.png, 12:49 PM): corner P1312, cyan banner "TRY AGAIN!", text "Fan-out identifies how many gates can be driven by the output of one gate." No other buttons visible. No OK button needed on either path. Nothing saved.

## Final Quiz first question (Fred, Oct 25 ~02:05 JST; guest clock 12:52-12:55 PM)
From P1312 Reader: F3, Alt+Up, Alt+Right x11 to P900 (Author, shots/l_a900b.png 12:52 PM), F3. Reader P900 (shots/l_r900.png, 12:53 PM): Lesson Menu layout differs from Author. Click "3. Final Quiz" -> P10004 (shots/l_p10004.png, 12:53 PM): FINAL QUIZ banner, orange "- Begin" and "- Directions". Click "- Begin" -> shots/l_q1.png (title "Nida Corporation - Logic Families", clock 12:54 PM): NO corner page label drawn. Top strip tabs "Testing", "Question 1.", "Time". Text "Noise is caused by an IC's _______" with four lettered orange buttons a-d: "output.", "switching.", "propagation.", "fan-out.". Bottom: three tab shapes (left, centre, right) peek above the taskbar, their labels are hidden (cannot read). Click b (shots/l_q1b.png 12:54 PM, l_q1c.png 12:55 PM, 35 s later): button b turns light cyan; page did NOT change; no CORRECT/wrong banner, no OK/Skip/Back visible. Nothing pressed after that, nothing saved.

## Final Quiz ten-question run (Reader level, Oct 25 2026): Bochs died at Q6, parked
All quoted from shots copied to new paths (shots/n_*). Title always "Nida Corporation - Logic Families"; tab "Testing" left, "Question N." centre, "Time" right. Clicking a choice letter button only highlights it; the OK strip (args 518 902) advances to the next question. No feedback banner, dialog or new page appeared after any OK.
- Q1 "Noise is caused by an IC's ____" - answered b, OK, advanced (1:01 PM).
- Q2 "Which IC has a slow switching speed?" (7400, 74H00, 74L00, 74S00) - answered c, OK, advanced (1:01 PM).
- Q3 "With a fan-out of 4, how many ICs can be driven?" (2, 4, 8, no limit) - answered d on purpose (wrong), OK, advanced (1:02 PM).
- Q4 "What is the most widely used logic family?" (TTL, CMOS, IIL, ECL) - answered a, OK, advanced (1:03 PM).
- Q5 "Which IC has a fast switching speed?" (74C00, 74H00, 74L00, 7400) - answered a, OK, advanced (1:04 PM).
- Q6 "Propagation of an IC is the amount of delay in _______" (fan-in., fan-out., switching., noise.) - clicked a (highlighted, shot n_q6_sel.png, 1:05 PM), then clicked the OK strip; Bochs process was gone afterwards (no shot after OK possible). Last page reached: Question 6. Nothing saved. Not reached: Q7-Q10, P10303.
Bochs is not running; no log error line. Parked.

## Final Quiz full run, second attempt (Fred, Oct 25, restored 01:51:26 JST from state-reader-p310; reached P10410 at 02:07:04, about 15.5 min, Bochs still alive)
Route: ctrl+o 9e954d01.tbk (opened on P10), F3 to Author, Alt+Up, Alt+Right x11 overshot to P1001 (Author), Alt+Left to P900, F3 to Reader (shots/o_r900.png, clock 11:50 AM); mouse capture was OFF after restore, toggled ON. "3. Final Quiz" -> P10004 (o_p10004b.png) -> "- Begin" -> Q1 (o_q1.png). One shot per question taken after OK (o_q{N}ok.png shows question N+1). The question order was the SAME as the first run for Q1-Q6, so no randomness seen there.
Answers: Q1 b; Q2 c; Q3 d (deliberately wrong); Q4 a; Q5 a; Q6: NONE (my click at x=150 missed the lettered button at x about 121; OK still advanced, so OK with nothing chosen is accepted); Q7 a (deliberately wrong); Q8 d; Q9 a; Q10 a.
Questions seen (tab "Question N.", title "Nida Corporation - Logic Families"): Q6 "Propagation of an IC is the amount of delay in ____"; Q7 "Which IC family has the lowest power rating?" (TTL, IIL, CMOS, ECL; o_q6ok.png 11:57 AM); Q8 "Which IC family has the lowest power requirements?" (TTL, IIL, ECL, CMOS; 11:57 AM); Q9 "The advantage of TTL over the ECL family is ____" (higher power., faster speed., slower speed., lower power.; 11:58 AM); Q10 "The advantage of CMOS over the TTL family is ____" (same four choices; 11:59 AM).
After Q10 OK: shots/o_q10ok.png, corner label "P10303", centre tab "End of Test", clock 12:00 PM, text "The test is complete and your score is 50%. Do you want to ________" with a "review the test?" and b "exit?" buttons (nothing selected). Score 50% with Q6 blank, Q3 and Q7 wrong, so at most 7 of the other answers could be right; I did not check which were right.
Pressed the bottom OK strip once at P10303 with neither a nor b chosen: shots/o_p10303_ok.png: corner label "P10410", "Review These Objectives:" with "1. TTL Integrated Circuits" and "2. Other Integrated Circuits", clock 12:00 PM (so OK leads to the review page, not the menu P900, because score was below 100%). Not pressed: Skip, Back, a/b buttons, anything on P10410.
Bochs death notes: first run died about 14 min after its restore (at Q6 OK); second run passed Q6 OK at 02:03 (about 12 min after restore) and lived to 02:07 (15.5 min). Death is not tied to the Q6 page or to a fixed time; nothing was different except fewer shots (no extra selection shots).

## P10410 review buttons (Fred, Oct 25 02:08-02:10 JST, same Bochs session, guest 12:01-12:04 PM)
- Clicked "1. TTL Integrated Circuits" twice (shots/p_ttl.png 12:01 PM, p_ttl2.png after 15 s 12:02 PM, p_ttl3.png second click 12:02 PM): nothing happens; corner label stays "P10410", title unchanged, no dialog.
- Clicked "2. Other Integrated Circuits" (shots/p_other.png, 12:03 PM): same, nothing happens.
- Reason from R.json (decoded, not observed): on P10410 the buttons standard1 and standard2 (rects the same as groups Review 1/Review 2) are enabled=0 with no script; the "Review N" fields have no script. So both are disabled placeholders (gold look) in this run. Whether they enable for other score/objective results: cannot read from this run.
- The only live control is the bottom-right "Menu" button (R.json id 13, script "buttonClick: gotoMenuPage()", rect 8152,6210,9352,6630 twips). Clicked its visible strip at args 1180 902: shots/p_menu.png shows corner label "P900", "LESSON MENU" with 1. TTL Integrated Circuits, 2. Other Integrated Circuits, 3. Final Quiz, Lesson Exit, clock 12:04 PM. Nothing else pressed; Bochs alive.

## Directions page and second quiz attempt (Fred, Oct 25 02:11-02:13 JST, guest 12:05-12:06 PM, same Bochs session)
- From P900 Reader I clicked "3. Final Quiz" and then "- Directions" (the P10004 step in between was clicked blind, not shot). shots/q_dir.png (12:05 PM): corner label "P10020", title "Nida Corporation - Logic Families". Text: "Directions" / "Read each question carefully before selecting an answer." / "There is only one correct response to each question." / "Choose the response that best answers the question." / "When all questions have been answered you will receive a score based on the number of correct responses." A cartoon teacher with a pointer on the right. No button readable on the page; two button tops peek above the taskbar, at bottom-left (RFB x 9-37) and bottom-right (x 603-631), labels hidden. P10020 is NOT in the decoded 9e954d01 page_list (cannot say which book it comes from).
- Clicking the bottom-left strip (args 46 902) returned to P10004 (shots/q_back.png, 12:06 PM: FINAL QUIZ, "- Begin", "- Directions"). The bottom-right strip was not pressed.
- Clicked "- Begin" again (shots/q_begin2.png, 12:06 PM): tab "Question 1.", text "What is the most widely used logic family?" (a TTL, b CMOS, c IIL, d ECL). Run 1 and 2 had "Noise is caused by an IC's ____" as Question 1, so the second attempt in the same session has a different question order (this was Q4 in the earlier run). Nothing answered. Bochs alive.

## 100% run and exit test (Fred, Oct 25 02:13-02:28 JST, guest 12:07-12:21 PM, same session, Bochs alive ~37 min since restore)
- Going out of the new attempt's Q1: Back strip (args 48 894 / 80 894) and Help strip (args 640 902/892/896) did nothing on Question 1 (shots/r_out.png, r_out2.png, r_help*.png, 12:07-12:09 PM; tip positions were near the strip but I cannot prove they hit it). So I just ran the test.
- Correct answers were taken from R.json: on each question page the hidden "Correct" rectangle's top y (1515/2490/3465/4440 twips) sits next to choice A/B/C/D. Checked against knowledge on P10215/P10216/P10210/P10226.
- Attempt order (tab, text, answer, shot): Q1 "What is the most widely used logic family?" a; Q2 "If an IC has a fan-out of 10, how many other ICs can it drive?" c "10" (r_q1ok.png 12:10 PM); Q3 "Which is not a military IC?" a 74F00 (12:11); Q4 "Which IC has a super fast switching speed?" d 74S00 (12:12); Q5 "Propagation of an IC is the amount of delay in ____" c (12:12); Q6 "Which is a military IC?" b 54L00 (12:13); Q7 "The advantage of ECL over the TTL family is ____" b faster speed (12:14); Q8 "Which IC family has the lowest power rating?" c CMOS (12:15); Q9 "Which IC family has input/output voltages ranging from 0 to 15 volts?" c CMOS (12:15); Q10 "The advantage of CMOS over the TTL family is ____" d lower power (12:16). One shot per question taken after OK (r_q{N}ok.png shows question N+1).
- P10303 (r_q10ok.png, 12:17 PM): corner "P10303", tab "End of Test", "The test is complete and your score is 100%. Do you want to ________" a "review the test?" b "exit?". Clicked b (r_exitb.png, hover cyan; no visible change otherwise), then OK strip (args 518 902): r_exitok.png (12:18 PM): corner label "P900", LESSON MENU with 1. TTL Integrated Circuits, 2. Other Integrated Circuits, 3. Final Quiz, Lesson Exit. "3. Final Quiz" is now drawn in a greyish-blue text (looks disabled/completed) while the others are black; it still opened P10004 when clicked (r_fq.png 12:18 PM). No dialog appeared.
- Part 1 (P10020 right strip): "3. Final Quiz" -> "- Directions" -> P10020 (r_dir3.png, 12:20 PM, same text as before). Clicked the bottom-right strip (args 1220 894, tip over the button top, checked with crop r_dir3h_c): r_dirright2.png (12:21 PM): corner label "P10004", FINAL QUIZ with Begin and Directions. So the right strip also goes back to P10004 (the left strip did earlier). An earlier right-strip try with a wrong Directions click proves nothing.

## Long-text pages (Fred, Oct 25 02:29-02:44 JST, guest 12:22-12:37 PM; Bochs alive ~53 min since restore)
Navigation: Reader Alt+Right does nothing, so F3 to Author, Alt+Up (lands on the 2nd page entry, P1), Alt+Right in batches of 12/12/12/8 with label shots (s_b1..s_b4: P1040, P1140, P1236, P1290), F3 to Reader for each page shot, F3 back. Reader shots (one per page): s_p1290.png, s_p1300.png, s_p1302.png, s_p1304.png, s_p2170.png. In Author view the catalog/tool palette covers the left of the page and the page is cut at the right, so only the Reader shots count.
- P1290 (12:30 PM, corner "P1290"): orange-framed pale panel, text "Which IC is part of the military group of TTL circuits?" on one line, fits with a wide margin, no scroll bar, nothing past the page edge. Below: three orange IC pictures 7408, 7400, 5408. Last readable line is the question itself.
- P1300 (12:31 PM): same layout, "Which of these ICs is the slowest?" Chips 74H00, 74S00, 54L00. Fits.
- P1302 (12:32 PM): blue panel with "TRY AGAIN!" tab: "The letter "H" in the ICs number identifies a fast switching speed / or short propagation delay." (two lines, fits, about 30 px margin right). Under chips 74L00, 54H00, 74S00 three captions: "- Low power consumption / - Longer propagation delays"; "- High speed switching / - More power consumption / than L type / - Short propagation delays"; "- Schottky circuitry / - Super fast / - Less power consumption / than H type". Last readable line: "than H type" (bottom of the third caption, y about 452), then the taskbar edge is just below at about 486. Nothing clipped that I can see; the page's bottom 30 px are hidden under the taskbar anyway.
- P1304 (12:32 PM): same page as P1302 with the text "The letter "S" in the ICs number identifies that this is a Schottky / IC. Schottky ICs have a super fast switching speed." Same captions, same last line "than H type". Fits.
- P2170 (12:37 PM): blue panel, "There are different families of ICs because some circuits require / speed while others require less power." Table in a brown box: FAMILY / SPEED (ns) / POWER (mw): TTL 10 10, IIL 10 10, CMOS 25 .00001, ECL 2 40. Last readable line: "ECL 2 40". Fits, no scroll bars.
- On every page small button tops peek above the taskbar at bottom-left (x about 15-35) and bottom-right (x about 610-630), labels hidden. Not chased. No scroll bars on any of these five pages.

## Lesson Exit test (Oct 25 02:46-02:42 guest 12:41-12:42 PM)
- Reached P900 in Reader (needed 11 Alt+Right after Alt+Up in Author; the first 10 stopped at P450). Shots shots/s_p900.png, t_exit1.png.
- Click "• Lesson Exit": ONE dialog "Are you sure you want to Exit the Lesson?" with Yes / No. Waited 10 s, no second dialog (t_exit1b.png).
- No: dialog closes, still on P900 (corner label P900), no further dialog (t_no.png). Lesson Exit button shows hover highlight.
- Lesson Exit again -> same single dialog (t_exit2.png). Yes: within 6 s the whole ToolBook window is gone, no other dialogs; Win98 desktop remains (icons incl. ToolBook II Instructor, TB80RTM), taskbar empty of tasks (t_yes1.png, t_yes3.png unchanged 12 s later).

## 70% run, "review the test?" (Fred, Oct 25 02:51-03:01 JST; restored pid 779985 at ~02:49; guest 11:48 AM-12:01 PM; Bochs alive)
- Route: restore, capture toggle, ctrl+o 9e954d01.tbk (opens P10 = 2nd entry), F3, Alt+Right x9 (no Alt+Up) -> P900, F3, Final Quiz, Begin (shots u_*). Table of every quiz page's correct letter and button x: /workspace/bochs/quiztab.json (from R.json).
- Order again Noise, slow switching, fan-out 4, most widely used, fast switching, propagation, lowest power rating, lowest power requirements, TTL over ECL, CMOS over TTL (same as first attempt after a restore). Q3 screen itself not shot (u_q2ok shots lost in capture), inferred from order.
- Answers: Q1 b ok, Q2 c ok, Q3 a WRONG, Q4 a ok, Q5 b ok, Q6 a WRONG, Q7 c ok, Q8 d ok, Q9 a WRONG, Q10 d ok.
- P10303 (u_q10ok.png, 11:59 AM): corner P10303, "End of Test", "your score is 70%". "a review the test?" text is beige/dimmed unlike "b exit?" which is white; a's icon is drawn differently (looks greyed). Clicked a (u_reva.png: no visible selection change), OK strip -> u_rev1.png (12:00 PM): corner P10410 "Review These Objectives:" with "1. TTL Integrated Circuits", "2. Other Integrated Circuits", same page as the 50% run. No question review screen, no Next/Back.
- Clicked both gold buttons once (u_rev_ttl.png, u_rev_oth.png, 12:00 PM): nothing changes, label stays P10410. No left bottom button visible; right-strip Menu returns to P900 (already known). Left-strip click attempt missed (pointer ended on Start, u_rev_left.png), nothing happened.
- Bochs left running on P10410.

## Plain-text body pages (Fred, Oct 25 03:06-03:16 JST; guest 12:01-12:15 PM; pid 779985 alive)
Route: from P10410 the Menu strip (args 1180 902) -> P900, F3, Alt+Right x2 -> P1040, +3 P1070, +12 P1170, +6 P1210, +48 (4x12, label check P1940 at 24) -> P2210; F3 for each Reader shot (shots/v_p1040, v_p1070, v_p1170, v_p1210, v_p2210.png). All in the cream-framed blue panel, text white, the same panel on every page (panel inner ~ x 50-595, y 103-228).
- P1040 (corner P1040, header tab "DISCUSSION"): line 1 "Transistor-Transistor Logic (TTL) is the most widely used family" (T, T, L, TTL in cyan), line 2 "of  integrated circuits." (double space after "of"). Text rows y 144-158 and 163-177. Below: IC 5400 and IC 7400.
- P1070 (corner P1070): one line "The Commercial group is recognized by the 7400 numbers." text rows y 163-177 (R.json text has 3 leading blank lines). Military/Commercial boxes below.
- P1170 (corner P1170): "For example, if an ICs fan-in is 1, that value is subtracted from the" / "fan-out of the driving IC." rows 144-158, 163-177. NAND gate diagram below.
- P1210 (corner P1210): "Notice, each TTL IC shown has a letter code included with the" / "number. The letter identifies the speed of the IC." rows 144-158, 163-177. Three ICs 74L00, 54H00, 74S00.
- P2210 (corner P2210): "Learn to use the IC data book, technical guide and cross" / "reference manual when replacing a defective IC.  Especially if" / "you intend to substitute a replacement IC for the original." rows 144-158, 163-177, 182-196. IC DATA BOOK picture below.
- Line pitch 19 px (rows start 144 -> 163 -> 182). Text left edge x about 75. Glyph rows 15 px tall incl. descenders. Text is bold-looking: vertical stems are 2 px wide (histogram: 2 px runs dominate), sans (Arial-like), size about 13-14 px. R.json field font is 0x644 but flags show no explicit bold (only P1040 runs have a flags 0x4 cyan run), so bold comes from the font entry, cannot confirm that from the record.
- Bochs left running on P2210 Reader.

## P1040 body text field properties + colour runs (Fred, Oct 25 03:24-03:44 JST; guest 12:29-12:42 PM; pid 779985; nothing changed, not saved)
Route: Author Alt+Left from P2210 in 12/12/6(aborted shell)/12/12/12/3 (labels P1940, P1310, P1170, P1040 checked; shots w_b*.png, w_p1040a.png 12:36 PM). One click at RFB (400,240) selected the field (w_sel.png: handles, corner P1040). props.sh w1040 (Shift+F6, tabs via Ctrl+Tab, shots g_w1040_0..4.png, 12:36-12:37 PM), dialog title "Properties for Text Field", window title "ToolBook II - 9e954d01.tbk".
- Name "Text", Layer 1 of 6, ID shown as 0.
- Draw: Border style Inset, Field type Word wrap, Draw transparent off, Draw baselines off, Visible on, Use custom colors (fill blue, stroke white-ish). 
- Bounds (page units): Left 600, Top 600, Width 8205, Height 1890.
- Font: Arial, Bold, 12; Underline/Strikeout off, Normal. Nothing marked as mixed (font and size boxes filled in).
- Paragraph: Alignment left, Line spacing single; Indents First line 360, Other lines 360, From right 310; Tabs Spacing 720, Type left.
- Behavior: tooltip empty; Enable the field on; "Lock the text and activate mouse events if the field is enabled". (Drag & Drop tab not opened.)
- Text-edit part: closed palette with its Close button, double-click on TTL gave a caret between the T's (w_dbl2.png, 12:39 PM), no handles. Shift+F6 then opens "Properties for Text" with a single Font tab, first line 'Typing font in Text Field "Text"': Arial, Bold, 12, Underline/Strikeout off, Normal, Text color box greyed (w_pal1.png 12:39 PM, w_pal2.png 12:40 PM after clicking in plain text, identical).
- Selected "TTL" (click before T, Shift+Right x3, w_sel3.png): palette title "Properties for Text", line 'Selected text in Text Field "Text"': Arial, Bold, 12, Text color swatch light cyan (w_pal3.png 12:41 PM).
- Selected plain text "s " of "is" (w_sel4.png): same 'Selected text...' dialog, Arial, Bold, 12, Text color swatch shows a dithered near-white/very pale pattern with cyan-blue dots, i.e. not a solid cyan; cannot tell if it is "no colour set" or white (w_pal4.png 12:42 PM).
- Palette closed again; Bochs alive, Author level, P1040, selection left inside the text (w_end.png).

## Final Quiz grey label on P900 (Oct 25, guest ~12:45-12:58 PM)
- P900 labels "1. TTL Integrated Circuits" and "3. Final Quiz" have light-blue/grey text; "2. Other ICs" and "Lesson Exit" are black. Seen in Author (x_a900.png), Reader (y_r0.png, y_r900g.png). Right after a fresh snapshot restore all four were black (u_r900.png).
- Not specific to a 100% run: it appeared after a 70% run + TTL page visits. 100% run NOT done this time (not needed to see it).
- Group "Selection T" (id 28): Properties for Group = Layer 7 of 8, Behavior "radio mutually exclusive"; Font Arial Bold size blank (mixed). Actions Editor (F5): one "On click..." row, no actions (File>Export Actions greyed). Closed with Alt+F4, no prompt, nothing changed (one dropdown arrow press changed selection to "On double-click" but Escape restored "On click").
- R.json statics: field "Selection T" (id 27) has style_runs [] and runs_handle 0xffff; fields 1 and 2 have one run (font 0x734, colour None). Button id 26 stroke #bfffff (Exit button stroke #ffff00, others black); all buttons enabled, state26 0xb. Group scripts: ButtonClick -> setSection("1"/"2"/"T") then go to P1001/p2001 or gotoQuizPage(). Field scripts: enter/leave handlers (hover pill), same for all four fields.
- Hover: moving over any label draws a white pill; text colour unchanged (grey stays grey, black stays black) (y_h1/h2/h3.png). Hover is not the cause.
- Persistence: closed the book (went via Help P20001 -> nida81.tbk), reopened 9e954d01.tbk fresh, walked P10 -> P450 -> P900 only: labels 1 and 3 still grey (y_r900g.png). So it is not in-memory book state; it survives reopening the book without save. Cause not found (not in the group scripts; probably progress saved by setSection/lesson/quiz code, in a file/INI/registry, or P900 enter-page code). Cannot read.
- Click label 3 -> P10004 (Begin, Directions; no label colours there), left strip button -> P900: label 3 and 1 still grey (y_q1.png, y_q2.png). Button art under the label is the same orange in all four; only text colour differs.
- Clicking label 2 -> P2001 (Discussion/Summary); its bottom-centre strip is Help (P20001 of nida81.tbk), whose back arrow stuck; recovered by reopening the book. Did not test whether label 2 turns grey after a lesson visit.

## CDBUNIONDAMAGE hit list, P420 -> P430 at Reader level (Fred, Oct 25 ~04:45-04:56 JST) - NO HIT, page never changed
- Address: `tools/ne_info.py` gives "ord 288 CDBUNIONDAMAGE seg 4:014c ghidra~1018:014c". Segment 4 selector this session = 0x2BAF (`info ldt`: one entry, limit 0x1b5f, ldt[0x575] base 0x803f7320; 0x575<<3|7 = 0x2BAF). Checked by bytes: 0x2baf:0x14c = `mov ax,0x35af; enter 0xa,0` (export entry); 0x2baf:0xee0 = `55 8b ec 83 3e 32 17 00` (FUN_1018_0ee0). Breakpoint: `vb 0x2baf:0x14c`, one breakpoint only.
- Static (not run-time): view pointer word = [bp+6] at entry, global ds:01e0 (read 0x43d0 earlier). Rect = 8 bytes at ss:[bp-10], built by FUN_1018_0b00 (call .+0x7e20), then passed to the first call at 0x2baf:0x18a (FUN_1018_026c, call target 0x758c). 026c calls 1a44 (clip) and pushes [bp-6],[bp-8],[bp-10],[bp-12] then calls 0ee0, so word 0 of the clipped rect is pushed last and is the SETRECTRGN left ([bp+4]); words 1,2,3 = top,right,bottom. (Ghidra's SETRECTRGN(param_4..param_1) order is reversed vs the real stack.) Not confirmed at run time because there was no hit.
- Start: Author P900 -> Alt+Left x4 -> P420 (shots/z_a420.png, 1:37 PM) -> F3 -> Reader P420, "before" shots/z_r420_before.png (corner label P420, clock 1:38 PM). blist empty before arming.
- Trial 1 (04:46:50): vb armed, Alt+Right at Reader: 0 hits in ~45 s, page still P420 (shots/z_r420_after1.png, 1:43 PM). Alt+Right does nothing at Reader (no menu bar).
- Trial 2 (04:52:34): vb armed, mouse pointer parked on the P420 Next strip (white hover pill seen under the pointer, shots/z_r420_after2.png) and one left click (held 1.5 s): 0 hits, page still P420 (1:50 PM). Two more clicks with breakpoint off (after3, after4, 1:50/1:51 PM): still P420.
- Trial 3 (04:54:50): vb armed, Page Down key at Reader: 0 hits, page still P420 (shots/z_r420_after5.png, 1:52 PM).
- Raw logs: logs/cdb_hits_run_click.log (trial 2), logs/cdb_hits.log (trial 3). Breakpoint deleted each time; final blist empty. Bochs left running at Reader P420, no snapshot.
- Hit table: empty (0 hits, no view pointer or rect words recorded).

### Addendum (Fred, Oct 25 ~04:58-05:10 JST): CDBUNIONDAMAGE breakpoint across page changes - still 0 hits everywhere
- Reader level P420 -> P430: changed during the Return or Space run (cannot say which), breakpoint `vb 0x2baf:0x14c` armed, 0 hits. After shot shots/z_after_space.png (P430, 1:57 PM). Earlier Reader tries with the breakpoint armed (Alt+Right, Page Down, Next-strip click) did not change the page.
- Author level walk (user's request): P400 (shots/w_start_p400.png, 1:58 PM) -> P410 -> P420 -> P430 -> P440 -> P430 -> P420 -> P410 -> P400, one Alt+Right/Alt+Left per step, one breakpoint armed each step, 25 s quiet window. Result: 0 hits on all 8 transitions. Corner labels / clocks from shots/walk_step{1..8}_after.png (copied to /tmp before reading): P410 1:59, P420 2:00, P430 2:01, P440 2:02, P430 2:03, P420 2:04, P410 2:05, P400 2:06 PM. Logs: logs/walk_step1..8.log. Breakpoint deleted after each step (blist empty).
- Conclusion so far: CDBUNIONDAMAGE (0x2baf:0x14c) is not called on any of these page changes, Reader or Author. Caveat: selector 0x2baf was derived from `info ldt` this session; bytes at 0x14c match, but I did not run a positive control (a case that is known to call it).

### Addendum 2 (Fred, Oct 25 05:10-05:20 JST): walk repeated with Frank's validity checks, linear breakpoint
- Breakpoint type: `lb 0x803f746c` (linear = ldt[0x575] base 0x803f7320 + 0x14c). Before every step the script re-read `info ldt` entry 0x575 and `x /7bx 0x2baf:0x14c`.
- Every step (1-8): ldt[0x575] = Code segment, base=0x803f7320, limit=0x1b5f (unchanged); bytes at 0x14c = b8 af 35 c8 0a 00 00 (mov ax,0x35af; enter 0xa,0), unchanged. No re-arm needed.
- Transitions and results (labels/clocks from shots/walk3_step{n}_after.png): P400->P410 (2:08 PM) 0 hits; ->P420 (2:09) 0; ->P430 (2:10) 0; ->P440 (2:11) 0; ->P430 (2:12) 0; ->P420 (2:13) 0; ->P410 (2:14) 0; ->P400 (2:15) 0. Wait: labels read P410, P420, P430, P440, P430, P420, P410, P400 in that order. Logs logs/walk3_step1..8.log. Breakpoint deleted after each step; final blist empty. No hit even once. Still no positive control.
