# Appendix L. Bochs

**Date:** 2026-10-20

The command card for the host that opened the lesson. Chapter 7.6 is the claim. Chapter 4.6 is what the stops showed. `maps/bochs-20261020.md` is that boot's selectors. This appendix is how to do it again.

## L.1 Why this host

Bochs runs the Win98 guest and holds the debugger outside it. A break does not need SoftICE, and it does not need a program inside Windows. Registers, the stack, and memory are what the CPU holds. The cost is speed.

## L.2 This machine

| Item | Value |
|---|---|
| Build | `~/bochs/bochs/build-dbg/bochs` (3.1, internal debugger). `build-rfb` is the VNC build and was not used. |
| Config | `~/bochs/vm/win98.bxrc` |
| Disk | `~/bochs/vm/win98.img` (2 GB flat, cylinders=4063, heads=16, spt=63) |
| Guest | Win98 SE, 128 MB, Pentium model, ips=50000000, i440fx, Cirrus VGA, PS/2 mouse |
| BIOS | `~/bochs/bochs/bios/BIOS-bochs-latest` and `/usr/share/bochs/VGABIOS-lgpl-latest` |
| Dumps | `~/bochs/vm/dump*/` |

Start:

```
~/bochs/bochs/build-dbg/bochs -f ~/bochs/vm/win98.bxrc -q -unlock -debugger -dbglog ~/bochs/vm/debug.log
```

`-debugger` opens `<bochs:N>` in the terminal. `c` runs the guest. Ctrl+C returns to the prompt. `-unlock` clears a stale lock left by a killed Bochs. `-dbglog` saves what the debugger prints, including a long `info ldt`.

The guest window and the terminal are separate. Click the window for the mouse and the keyboard. Ctrl+F10 toggles the mouse. Read the terminal before the window. A missing BIOS is a panic there, not a Windows error.

## L.3 Files into the guest

```
cd ~/<folder>
genisoimage -o ~/files.iso -J -R .
```

Point `ata0-slave` in `win98.bxrc` at that ISO with `status=inserted`, then restart. Copying a file back out of the guest has not been needed. The `genisoimage` flags were not re-tested this session.

## L.4 Commands that worked

| Command | What it does |
|---|---|
| `vb 0xSEL:0xOFF` | Break at a live selector:offset. |
| `info break` | List breakpoints. The numbers are what `bpd` and `bpe` use. |
| `bpd N` / `bpe N` | Disable or enable breakpoint N. |
| `c` | Continue. One command per line. |
| `r` | Registers. A 16-bit read is the low half: AX, DX, not EAX. |
| `print-stack N` | N stack words. Addresses are linear. |
| `info ldt A B` | LDT entries by decimal index. `2333 2333`, not `0x48ef>>3`. |
| `x /20xb ADDR` | Bytes at a linear address. Not selector:offset. |
| `writemem "file" ADDR LEN` | Save guest memory. The folder must already exist. Stops at the first unmapped page. |
| `source file` | Run a command file. Absolute path. |

Not used, so not trusted: `del N`, `lb`, `trace on`, `show call`, `loadmem`. There is no debugger command for a full physical RAM dump. The GUI Suspend hung. Do not use it. Kill with `kill $(pgrep -n bochs)` and start again with `-unlock`.

## L.5 Reading a stop

Bochs prints `Breakpoint K`, the selector:offset, and the instruction.

At a function entry the first two stack words are the return address: offset, then segment. The arguments follow, nearest the top first. That order matches a Ghidra `__stdcall16far` signature.

```
print-stack 24
  STACK 0x80477ac0 [0x0a60]   return offset
  STACK 0x80477ac2 [0x38f7]   return segment (11B0 this boot)
  STACK 0x80477ac4 [0x0c36]   first argument
```

A far pointer comes back in DX:AX. A word comes back in AX. To catch the return, break on the instruction after the call. `28FF:02E5` was the instruction after the `03C8` lookup on this boot.

## L.6 Selectors after a reboot

Windows assigns an LDT selector when the NE segment is loaded. The numbers change every boot. Only a segment that has been touched has a real entry.

1. Start with `-dbglog`. Open the lesson so TB80BAS loads.
2. `info ldt`. Match Ghidra segments by size, not by the index formula.
3. Confirm with a relocation. A far call in the file has the Ghidra selector (`0x10B0` and the rest). The same word in the loaded bytes has the live selector.

The table for the boot of 2026-10-20 is `maps/bochs-20261020.md`. Do not reuse it.

## L.7 One object load

Set these only after the lesson has been opened once, so the segments exist. Then open the page. The selectors are the 20 October boot.

```
vb 0x2a37:0x2174   book open
vb 0x2907:0x08b2   reader creator     handle, 0x096c, err
vb 0x391f:0x04da   entry read         reader far, 2, entry far, slot, err
vb 0x391f:0x08d6   read setup
vb 0x291f:0x02cc   file read          len, dest off, dest seg, pos lo, pos hi, file, err
vb 0x28ff:0x02ce   send message       0, 0, msg, class word, block, handle, err
vb 0x28ff:0x03c8   handler lookup
vb 0x28ff:0x02e5   lookup returned    DX:AX is the handler
vb 0x2907:0x0aeb   after message 0xE
```

Every object hits several of these. `bpd N` silences a stop that is already understood. The handle (`0x0C1E`, `0x0C36`, `0x0C4E`) names the object. Those three are `0x18` apart.

To dump the record: at `08D6`, note the block selector. After `02CC` returns, `info ldt N N` for that selector's decimal index, then `writemem` the base for `limit + 1` bytes.

The on-disk copy of entry index `I` is at file `0x10D6 + 24 * I`.

## L.8 Pitfalls

| What happened | What to do |
|---|---|
| Bochs will not start. Files locked. | Add `-unlock`. |
| Panic reading a ROM image. | The BIOS path in the config is wrong. Read the terminal. |
| Guest window stays small. | This X build does not scale. Not solved. |
| Mouse stuck on the zoom tool. | That was the desktop magnifier. Click the guest. Ctrl+F10. |
| `syntax error at print-stack` | More than one command was pasted. One line at a time. |
| `writemem` writes nothing. | The folder is missing, or the address is unmapped. `mkdir` first. `info ldt` first. |
| Suspend hangs. | Do not use it. Kill Bochs. Restart with `-unlock`. |
| The dump is the wrong segment. | The first data dump used LDT index 1161. The data segment was `3477` this boot. |
| The bytes look right and the selector is wrong. | Selectors changed. Section L.6. |

## L.9 Still to capture

Each of these needs the lesson opened again, so the selector map comes first.

1. The dispatcher `03C8` returns for handle `0x0C36`. The return already captured was handle `0x0C1E`, which is not the 412-byte record.
2. Twenty-four bytes of the live entry. On this boot that was `x /24xb` at the `3E67` base plus `0x0C36`. The file's last four bytes are `00 21 25 00`. They have not been seen in memory.
3. The file record at slot `0x096C` and file-table offset `0x0AE0`, with the book open, including the class-table pointer at `+0x163`.
4. The class table that pointer names.
