# Appendix G — SoftICE

The command card for the Windows 98 sessions. SoftICE and the Watcom debugger do not share a syntax. Do not type these lines into WDW. Appendix H is that debugger.

**Date:** 16 October 2026

SoftICE field work as the standing host closed on 11 October 2026. The kit that loaded was `SI405w9x` plus ICEDUMP 6.021, loader `w9x/4.05.334/icedump.exe`, and only after `winice.dat` listed the exports of both `kernel32.dll` and `user32.dll`. The night of 15 October still needed this card. The book-open read below is that night. The host was the Win98 VM. XP NTVDM is not a clean 16-bit host.

## G.1 The screen

Ctrl-D pops SoftICE over Windows. Ctrl-D again returns to Windows if the machine is running. While it is popped, Windows is stopped.

The screen is four regions, top to bottom, and you can turn each one on or off:

| Region | What it is | Command that toggles it |
|---|---|---|
| Register | AX BX CX DX, SI DI BP SP, DS ES SS CS IP, and the flags | `WR` |
| Data | Hex on the left, ASCII on the right. This is where a dump lands. | `WD` |
| Code | The disassembly at CS:IP. The current instruction is highlighted. | `WC` |
| Command | One line at the bottom. History with the up arrow. | always there |

There is no Locals pane and no Calls pane. The stack is memory at SS:SP. The frame, after `ENTER`, is memory at SS:BP. If you want a call chain you walk return addresses yourself, or you use the Watcom Calls window (Appendix H). SoftICE will not draw it for you.

`MAP` output is a list of segments for one module. The segment numbers in that list are hex. The selector beside each segment is this boot only.

## G.2 Commands that were actually used

Clear before you set. A breakpoint left over from the polygon painter (`GDI!POLYGON`, or BAS `1408:0376`) freezes SoftICE as soon as a page scrolls.

```
BC *
BL
```

`BC *` clears every breakpoint. `BL` lists what is still set. `BC n` clears one, by the number `BL` printed. `BD n` disables one without deleting it. `BE n` enables it again.

Break on an export. The ordinal form survives a reboot. A selector does not.

```
EXP TB80BAS
BPX TB80BAS.Ordinal_8
BPX TB80BAS!OBJFILEOPEN
```

`EXP` lists the exports. Ordinal 8 is `CDBFILEOPEN` on every boot. The `!` is SoftICE’s module mark. Watcom uses `@` for the same idea. `BAS(82)` and `BAS(83)` are not addresses. SoftICE rejects them.

Break on a live instruction, and do something when it hits:

```
MAP TB80BAS
BPX <selector>:0376 DO "D SS:BP-4 L 4; D DS:30AC L 40"
```

`MAP TB80BAS` prints the live selector for each NE segment. You read the selector for the segment you want, then you type that selector. `DO` runs the quoted commands and, unless one of them stops, continues. `D` is a dump. `L` is the length. `SS:BP-4` is the saved word just under the frame. `DS:30AC` is the point buffer the polygon painter copies into.

Run and step:

| Command | Effect |
|---|---|
| `G` | Go. Run until a breakpoint or a fault. |
| `T` | Trace. Step into a `CALL`. F8 is the same key. |
| `P` | Proceed. Step over a `CALL`. F10 is the same key. |
| `P RET` | Run until the next `RET` or `RETF` in this frame. This is how you leave a function without tracing every instruction inside it. |
| `U <addr>` | Unassemble at an address without moving CS:IP. |
| `R` | Show the registers. `R AX=1` sets one. |

Dump:

| Command | Effect |
|---|---|
| `D <addr>` | Dump bytes at a far address. |
| `D <addr> L <n>` | Dump `n` bytes. |
| `DB`, `DW`, `DD` | Bytes, words, dwords. A word dump is the one that matches a stack slot. |
| `D SS:BP+6` | The first stack argument after a far frame. See Appendix I for why `+6`. |

`/DUMP`, from ICEDUMP, writes the SoftICE console unless the dump experts are set. It does not write the address you think you named. A file that starts with the command log, or with the DOS device chain (`CON`, `AUX`, `PRN`), is not a book. A dump is real when it contains book strings at offsets already known. `page.bin01511` did: `ASYM_TpID`, `Page#`, matching `9e954d01.tbk` at `0xB8B51`.

Do not search all of memory for a byte pattern. A wide search for `80 65` GPFed the VM.

## G.3 What not to step into

A GPF in this host is usually a segment that is not present, or a far call into `KERNEL` that you traced into.

- Do not `T` into an unloaded NE segment. `MAP` the module first. If the segment is not in the list, it is not in memory. Set the breakpoint and `G` until the program loads it.
- Do not `T` a far `CALL` into `KERNEL`, `USER`, or `GDI` unless that segment is already present. Use `P`.
- The CMP expand host died in `TB80W16` at `001c:00000015` on the bytes `9A 9C 06 57 2A` (a far call, segment not present). That fault is parked. It is not the book-open path.
- `TBCBT` segment 7 holds the cipher exports. A module list that showed segments `01`, `0E`, `02`, `0B`, `08`, `0D`, `04`, `03` had not loaded segment 7. Breaking there before it is mapped faults. Searching memory for the leftover constants `0xA01` and `0x300` finds the call site while segment 7 is still unloaded.

If SoftICE will not pop, or the VM is wedged, the fallback on that VM is DEBUG.COM. It is a smaller language. `T` traces. `D` dumps. There is no `P`, no `BPX`, no `DO`, and no module name. `Q` quits DEBUG. Do not type SoftICE lines into it.

## G.4 The 15 October book-open read

This is the path that was on the screen, from the call that asks for 4 bytes down to the buffer those 4 bytes were not.

The stable names, in order:

1. `CDBFILEOPEN` is BAS ordinal 8. Break there on a lesson open. Do not break ordinal 51. Ordinal 51 is `CDBSENDCREATE`, the author create path. A lesson does not call it.
2. From there the open goes through `CDBCREATEBOOKREF`, then `FUN_1048_1cc4`, then `FUN_1048_2174`, then `OBJFILEOPEN`.
3. `OBJFILEOPEN` calls `FUN_1160_03de`. That function is the read wrapper. On that boot the call site was `36E7:201B` and the callee was `36F7:03DE`.

Those selectors died at the next reboot. The NE numbers did not. `36E7` was NE segment `2F` (Ghidra `1170`). `36F7` was NE segment `2D` (Ghidra `1160`). The check is `(NE index − 1) × 8 + 0x1000`. Segment `0x2D` is 45 decimal, and `(45 − 1) × 8 + 0x1000 = 0x1160`. The breakpoint that survives the reboot is not a selector and not a segment number. It is `BPX TB80BAS!OBJFILEOPEN` or `BPX TB80BAS.Ordinal_8`, then `T` into the `CALL`. `BPX BAS(2D):03DE` is the notation already rejected. `MAP` gives the selector. The offset `03DE` is the part you copy.

At the call site the bytes were:

```
36E7:2019  PUSH 04
36E7:201B  CALL 36F7:03DE
```

`PUSH 04` is the length. Four bytes. The far pointer to the buffer is already on the stack under it.

`FUN_1160_03de` begins with `ENTER 0022,00`. Until that instruction has executed, SS:BP is still the caller’s frame. Dumping `SS:BP+6` at the call site dumps the caller’s locals. That was the first wrong dump of the night. Step in with `T` once so CS:IP lands on the callee, `T` again past `ENTER`, and only then dump.

```
T
T
DW SS:BP+6 L 1
DW SS:BP+8 L 2
```

On that hit, `[BP+6]` was `0004`. The far pointer at `[BP+8]` was `3DD7:9086`. Dumping that address:

```
DB 3DD7:9086 L 4
DB 3DD7:9070 L 30
```

The four bytes were `FC B5 BD B0`. That is an internal pointer sitting in the buffer, not a page header. A page header that is the book signature is `03 4A 42 4F` (`JBO`, with a length byte in front). A record header that is the one being hunted starts `14 00`. Neither of those was in the four bytes. The wider dump showed `4F 46` (`OF`) nearby, at `9092`. Nearby ASCII is not the bytes you just read. Read the four at the pointer, then stop.

Inside `FUN_1160_03de` there are two ways to satisfy the read:

- At offset `048F` it calls `FUN_1258_00a8`, the buffered path.
- The next test, at `049A`, is `JZ 0516`. When the buffer already held the bytes, that jump was taken.
- Offset `04F3` is the raw DOS read (INT 21h, AH=`3F`). It was skipped. Setting a breakpoint only on `04F3` and watching it never hit is the correct observation. It is not a broken breakpoint.

So a 4-byte read that returns `FC B5 BD B0` is the wrapper doing its job on something that is not yet a record. The next useful hit is the same function again, on a later call, when the length is larger than 4 or the buffer starts with `14 00` or with `03 4A 42 4F`. Do not single-step the whole of `FUN_1258_00a8` looking for a compare against `0x14`. Chapter 4 already closed the static candidates. The live test is the buffer about to become an object.

## G.5 A session, in order

```
BC *
MAP TB80BAS
BPX TB80BAS!OBJFILEOPEN
G
```

Open the lesson. When it breaks:

```
T
```

only if the highlighted instruction is the `CALL` you mean to enter. Otherwise `P`. When CS:IP is inside `FUN_1160_03de` and past `ENTER`:

```
DW SS:BP+6 L 1
DW SS:BP+8 L 2
DB <segment>:<offset> L 10
```

Write down the length and the first bytes. `G` to the next hit. If the machine faults, `BC *` before you set anything else.

## G.6 What transfers to Watcom

The discipline transfers. The words do not.

- Break a stable export, not a selector copied from last boot.
- Dump the frame only after `ENTER`.
- Step over `KERNEL`. Do not trace into a segment `MAP` did not list.
- A 4-byte buffer that is not `14 00` is data. Record it and continue.
- Ordinal 51 is the wrong function.

Appendix H has the Watcom words for each of those.
