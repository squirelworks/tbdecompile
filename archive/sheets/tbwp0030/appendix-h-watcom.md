# Appendix H — The Watcom Debugger

WDW, the Open Watcom windowed debugger, on the same Windows 98 image. This is the host used after 11 October 2026. It is not SoftICE with different punctuation.

**Date:** 16 October 2026

ToolBook’s NE images have no Watcom debug info. WDW can see export names. It cannot see types, locals, or line numbers. The Locals window stays empty on `TB80BAS` and `TB80RTM`. You read the stack the same way Appendix I describes, or you do not learn the arguments.

## H.1 The screen

WDW is a Windows program. It does not pop over the machine the way SoftICE does. The lesson runs in another window. When a breakpoint hits, that window freezes and WDW comes forward.

The Windows menu opens the panes that matter. Leave the ones you are not using closed. A full set of them hides the instruction you meant to read.

| Pane | What it is for |
|---|---|
| Assembly | The bytes at CS:IP. This is the pane that matches Ghidra. Source will be blank. |
| Registers | AX through IP, and the flags. CS:IP is the instruction in the Assembly pane. |
| Functions | Export names for the module you have open. Right-click a name to break on it. This works when the command line will not resolve the name. |
| Break | The breakpoints that exist. Resume is a property of a row in this list. |
| Calls | The return addresses above the current frame. Chapter 12’s spine was read out of this pane. |
| Log | Status lines. `log <file>` copies this pane to disk. |
| Memory / data | A hex dump. Use it when you have stopped. The log does not capture it. |
| Locals, Watch, Source | Empty on these NE images. Opening them does not create symbols. |

The command line is a pane of its own, usually along the bottom. The keys that match the words:

| Key | Word | Effect |
|---|---|---|
| F5 | `go` | Run until a breakpoint. |
| F8 | `trace` | Step into a call. |
| F10 | `step` | Step over a call. |

If a key does nothing, type the word. Do not invent a SoftICE key. There is no Ctrl-D. `P`, `T`, `BPX`, `BC *`, and `!` are SoftICE. Typed here they are errors, or they are the wrong program.

## H.2 Commands

Module mark. SoftICE writes `TB80BAS!OBJFILEOPEN`. WDW writes `TB80BAS@OBJFILEOPEN`. The `@` is not optional when more than one module exports a similar name.

Break, then resume. `resume on` is not a flag you put on the creation line. It is a property of a breakpoint that already has a number.

```
break TB80BAS@OBJFILEOPEN
break 1 resume on
```

`BL` is not the list command here. The Break pane is the list. The number in `break 1` is the row in that pane.

If `@` fails, the DLL is loaded but WDW did not bind the export to the command line. Two ways that worked:

1. Functions pane, find the name, right-click, Break. Then in the Break pane turn Resume on.
2. Use the live selector from a hit you already trust.

```
break 44CF:0DE8
break 1 resume on
```

That selector is dead after a reboot. The export name is not.

Log, then continue. WDW has no “trace every call.” SoftICE’s `BPX … DO "…"` and WinDbg’s `wt` do not exist here. You name the functions. Each hit writes a status line and, with resume on, does not stop.

```
log c:\tbk\trace.log
break OBJFILEOPEN resume on
break CDBCHUNKFIND resume on
break CDBCHUNKLAST resume on
```

`log >> c:\tbk\trace.log` appends. `log` with no file stops logging. Close the log before you copy it off the VM. An open log is still growing.

`break <symbol> do <cmd>` runs a command on the hit. `hook <event> <cmd>` runs a command on a window event. Hook events are window events. They are not function entry. Do not use a hook to find the record reader.

The log line is a status line. It is not the registers and it is not the buffer. To see bytes, leave resume off on that one breakpoint, stop, and read the Memory pane at the address in DS:DX or at SS:BP+8. Then `go`.

## H.3 What the three traces contained

These were full passes with resume on, named exports only. Counts are hits, not functions.

| Trace | Hits | What fired | What did not |
|---|---|---|---|
| W16 | 11 | `GETPLATFORMREF`, `IS32BITENV`, `GETRUNTIMELOCALIZEDDLL`, `ACXINITIALIZETOOLBOOKSUPPORT`, `ACXOLEINITIALIZE`, the 32-bit thunk (`LOADLIBRARYEX32W`, `GETPROCADDRESS32W`) | A book open. A record walk. |
| UTL | 53 | String and task helpers, `PLUGINSVCINIT`, `TBK.INI` profile reads, metrics, `GHEAPCREATE` | A record walk. The type-name table lives in UTL and was not what those hits were doing. |
| BAS | 173 | `VALUETOSTRING`, the `VALUENEW*` family, `OBJFILEOPEN` (the frame was `enter 025A`), `STACKGETSIZE`, `STACKPUSH`, `CDBCHUNKLAST`, `CDBCHUNKFIND`, `CDBCHUNKEND`, `RESMGR*` | A compare of a far pointer against `0x14`. Ordinal 51. |

`OBJFILEOPEN` firing is the file-open path. It is not, by itself, the reader. The buffered read under it is `FUN_1160_03de`, and the raw DOS path at offset `04F3` is skipped when the buffer already has the bytes. That is the same fact as Appendix G.4, watched from the other debugger.

Another pass over the same W16 and UTL exports will produce the same log. Do not schedule one.

## H.4 The Calls window is one boot

On 15 October the Calls pane showed the same frames on almost every stop during book open and the page walk. Selectors from that pane:

| Selector:offset | Note |
|---|---|
| `3497:03EF` | Early frame. |
| `3497:4A6E` | The step point that was planned off this frame. |
| `3197:0379` | |
| `3167:0CB1` | Near call. |
| `3167:14BC` | Far call. |
| `3247:02BF` | Near. |
| `3247:05B7` | Near. |
| `3247:0B7A` | Far. |

The full table for that boot is `TBdecompile/maps/wdw-to-ghidra.md`. It is a lookup for those selectors. It is not a map of the next boot. Match an offset to Ghidra. Remap the selector with the Functions pane or with a fresh break on the export.

## H.5 Where to break next

1. `break TB80BAS@CDBFILEOPEN` on a lesson open. Resume on, so the open finishes far enough to load the book.
2. Then a stop, not a log, on `CDBCREATEPAGEREF` or `CDBSETVALUEEX`. Export names. Not the selectors in the table above.
3. When an object exists, dump the word at object `+0x0F` and the file offset the read just returned. That pair is the reader’s output. The function that produced it is the reader.
4. Do not break ordinal 51. Do not break `GDI!POLYGON` and leave it set. The second of those is a SoftICE lesson, and it still applies: a paint breakpoint you forget to clear will stop you on every scroll.

## H.6 A session, in order

```
log c:\tbk\open.log
break TB80BAS@CDBFILEOPEN
break 1 resume on
go
```

Open one lesson. When the log shows `CDBFILEOPEN` and the book is up, stop the machine (Break, or a second breakpoint you left with resume off). In the Calls pane, write down CS:IP and the first return address. In the Memory pane, dump the buffer pointer you get from Appendix I’s frame, not from a selector copied out of this appendix.

```
log
```

That closes the file. Copy `open.log` off the VM before the next run overwrites it.

## H.7 Faults, same as SoftICE

WDW will happily trace a far call into a segment that is not present. The result is the same GPF. `step` over `KERNEL`, `USER`, and `GDI`. Do not `trace` them. If the Assembly pane shows a selector that `MAP` would not have listed, that instruction is not yours to enter.

The CMP expand fault at `TB80W16` `001c:00000015` is the same parked fault as in Appendix G. It is not this spine.
