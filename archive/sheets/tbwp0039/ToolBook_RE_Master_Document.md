# ToolBook Engine Reverse Engineering: Consolidated Master Document

**Target module:** `TB80BAS.DLL` (16-bit Win16 runtime; companion `TB80RUN.EXE`)
**Compiler / architecture:** Watcom C, x86 real-mode / segmented
**Tooling:** Ghidra static analyzer, 86Box 6.0 emulator (build 9001), Open Watcom Windowed Debugger (WDW)
**Objective:** Isolate the unnamed stream walker, the `14 00 00` length parser, and the `0x76` live object hook.

This document merges four source files: the Session Summary PDF, the Engineering Manual PDF, the Reverse Engineering Report PDF, and the Session Log markdown. Every fact below comes from those sources. Where the sources differ or leave something out, it is flagged in section 14.

---

## Table of contents

1. Executive summary
2. Key findings at a glance
3. Background: why this target is hard
4. Phase 1: Architectural boundaries and live trapping
5. Phase 2: Live stack triage and call interception
6. Phase 3: Assembly analysis of the stream walker
7. Phase 4: Static decompilation and Ghidra mapping
8. Decompiled logic of the Master Record Reader
9. Ghidra decompiler recovery matrix
10. Phase 5: Fixing Ghidra's auto-analysis pipeline
11. WDW debugger syntax reference
12. Step-by-step reproduction guide
13. Glossary
14. Discrepancies, gaps, and open items
15. Suggested next steps

---

## 1. Executive summary

The sessions mapped the core asset-loading path of the legacy ToolBook engine. Static decompilation in Ghidra was paired with live instruction tracing in WDW running inside 86Box. Three landmarks were located and validated:

1. **Master Record Reader** (`FUN_1048_18c4`). It orchestrates file streaming, handle locking, and stream lifetime state.
2. **`14 00 00` Length Parser** (`FUN_10c8_00de`). It parses length-prefixed chunks from the raw stream.
3. **`0x76` Live Object Hook** (structure offsets `0x2E` / `0x30`). It points at the sub-stream structures where live text-property frames and `0x76` runtime objects are handled.

File parsing runs downstream of `CDBFILEOPEN` (`1048:017a`) and finishes before the paint loop, which is bounded by `CDBPAINTCLIENT` (`1010:0506`). A live trap on `OBJFILEOPEN` (`35A7:177F`) exposed the caller at `2A4F:21AD`. The traced file was `C:\TBK\9E54D01.TBK`. Directly after the open call, the engine checks `cmp byte ptr ss:[bx], 09` to tell length-prefixed structures from standard text streams.

Ghidra's decompiler output is badly fragmented because Watcom passes arguments in registers. The fix is a custom `__watcall` prototype in the processor's `.cspec`.

---

## 2. Key findings at a glance

| Component | Ghidra ID / Address | Role |
| :--- | :--- | :--- |
| Master Record Reader | `FUN_1048_18c4` | Orchestrates file streaming. Acquires the handle through `OBJFILEOPEN`, locks memory with `OBJLOCK`, and runs the main loops. Releases frames through `GLOBALUNLOCK`. |
| `14 00 00` Length Parser | `FUN_10c8_00de` | Low-level validator and parser for length-prefixed blocks. Reached through `call near ptr 0x0BDC` at `3FAF:25C4`. |
| `0x76` Live Object Hook | Offsets `0x2E` / `0x30` | Seen as `OBJLOCK(*(undefined2 *)(iVar2 + 0x2e), ...)`. Handles live text property frames and `0x76` runtime objects. |
| Entry anchor | `CDBFILEOPEN` at `1048:017a` | Start of the load window. |
| Exit anchor | `CDBPAINTCLIENT` at `1010:0506` | End of the load window. |
| Caller of `OBJFILEOPEN` | `2A4F:21AD` | Far-return address captured from the stack. |
| `OBJFILEOPEN` breakpoint | `35A7:177F` | On the `enter 025A, 00` prologue. |
| Type validation | `cmp byte ptr ss:[bx], 09` at `21BA` | Selects the length-prefixed parser path. |
| Sample asset | `C:\TBK\9E54D01.TBK` | File seen in the string pool. |

---

## 3. Background: why this target is hard

### 3.1 No export symbol for the stream walker
The walker that pulls object layouts out of `.TBK` files is an unexported sub-routine. Static listings show it only under compiler-generated labels such as `FUN_...`. It had to be found from the order of API entry points around it.

### 3.2 Watcom's register calling convention
Watcom C optimizes by passing parameters in registers, mainly `AX`, `DX`, `BX` and `CX`. Ghidra's x86 16-bit defaults assume a stack-based Pascal or cdecl model. The result is:

- invented stack frames anchored on `unaff_BP`
- loose, fragmented helper functions
- decompiler views that keep showing broken stack representations, even after a re-analysis, because of cached results

### 3.3 Redraw noise during live tracing
Breakpoints placed at `CDBPAINTCLIENT` fired inside asynchronous Windows input loops (`USER.EXE` handling `DISPATCHINPUT`, `RELEASECAPTURE` and `GETCURSORPOS`). Mouse movement kept triggering repaints, which hid the sequential loading phase.

---

## 4. Phase 1: Architectural boundaries and live trapping

### 4.1 Execution window
| Anchor | Symbol | Address |
| :--- | :--- | :--- |
| Entry | `TB80BAS@CDBFILEOPEN` | `1048:017a` |
| Exit | `TB80BAS@CDBPAINTCLIENT` | `1010:0506` |

File parsing happens fully after the entry anchor and before the exit anchor. Redraw events caught during idle-loop activity were filtered out so the trace covers only the loading phase.

### 4.2 Breakpoint scripting
WDW rejected modern block-style scripting. The syntax that failed (GDB or WinDbg style) was:

```text
break TB80BAS@CDBCREATEPAGEREF { resume on; log cdb_trace.log "Hits" }
```

WDW treats that as an expression error and does not support redirecting log output to a file path this way. The working form uses simple braces, an explicit `log` string, and a trailing `go`. Output streams into the native WDW Log Window (ALT+6):

```text
b TB80BAS@CDBFILEOPEN
b TB80BAS@CDBCREATEPAGEREF { log "Hit PageRef"; go }
b TB80BAS@CDBSETVALUEEX   { log "Hit SetValue"; go }
b TB80BAS@OBJFILEOPEN     { log "Hit ObjOpen"; go }
b TB80BAS@CDBPAINTCLIENT
```

The session log adds `bc *` first, to clear all existing breakpoints before setting these.

---

## 5. Phase 2: Live stack triage and call interception

### 5.1 Correcting the capture point
The first captures at `CDBPAINTCLIENT` landed in user-input loops and were discarded. The fix was to trap `OBJFILEOPEN` at `35A7:177F`, directly on its `enter 025A, 00` instruction. At that moment the stack frame has not been allocated, so the registers and stack still hold the caller's untouched state.

### 5.2 Register snapshot at halt
```text
AX: 3ECF   BX: 4780   CX: 16D7   DX: 0800
SI: 9820   DI: 0000   BP: 945E   SP: 9418
IP: 177F   CS: 35A7   FL: 0302   SS: 4857   DS: 3ECF
```

### 5.3 Stack analysis (segment `SS:4857`)
Reading raw memory at the top of the stack (`SP = 0x9418`) gave the 16-bit far return address:

```text
0x9414: 20 01 00 00   AD 21 4F 2A   80 00 ...
                      ^^^^^ ^^^^^
                      offset  selector
Return offset:   21AD
Segment selector: 2A4F
```

**Return anchor: `2A4F:21AD`.** This is the hidden call site inside `TB80BAS.DLL`.

### 5.4 Asset path extraction
The string pool near `0x93E4` in the local buffer holds:

```text
43 3A 5C 54 42 4B 5C 39 45 35 34 44 30 31 2E 54 42 4B
C  :  \  T  B  K  \  9  E  5  4  D  0  1  .  T  B  K
=> C:\TBK\9E54D01.TBK
```

---

## 6. Phase 3: Assembly analysis of the stream walker

Navigating to `2A4F:21AD` exposed the validation framework of the streaming engine.

```asm
; --- Argument setup ---
219C push word ptr 0E[bp]       ; asset file path pointer
219F push word ptr 0C[bp]       ; file mode / allocation flags
21A2 push word ptr 0A[bp]       ; workspace descriptor handle
21A5 push word ptr 08[bp]       ; length boundary parameters
21A8 call far ptr OBJFILEOPEN   ; request file handle from OS

; --- Return point ---
21AD mov  word ptr -2C[bp], ax  ; store returned handle / status
21B0 or   ax, ax                ; 0 = clean execution
21B2 je   21B7                  ; success: go to layout parser
21B4 jmp  near ptr 22DE         ; failure: error handler

; --- Property type validation ---
21B7 mov  bx, word ptr 10[bp]   ; pointer to current Object Descriptor array
21BA cmp  byte ptr ss:[bx], 09  ; type signature 0x09 property
21BE je   21C3                  ; match: main parsing loop
21C0 jmp  near ptr 23A8         ; mismatch: alternative type parser
```

### 6.1 Reading the flow
1. The caller pushes four values, then makes a far call to `OBJFILEOPEN`.
2. The return value in `AX` is stored at `-2C[bp]` and tested. Zero means success.
3. A non-zero value jumps to the error handler at `22DE`.
4. On success, the descriptor array pointer at `10[bp]` is loaded and its first byte compared with `0x09`.
5. A match goes to the length-prefixed parsing loop at `21C3`. A mismatch goes to the alternative parser at `23A8`, which is the path for standard text streams.

---

## 7. Phase 4: Static decompilation and Ghidra mapping

| Logical component | Ghidra block | Structural indicator |
| :--- | :--- | :--- |
| Master Record Reader | `FUN_1048_18c4` | Orchestrates `OBJFILEOPEN` handle creation, runs the main `OBJLOCK` loops, and releases frames with `GLOBALUNLOCK`. |
| `14 00 00` Length Parser | `FUN_10c8_00de` | Called through `call near ptr 0x0BDC` at `3FAF:25C4`. Iterates over data lengths to extract raw strings. |
| `0x76` Live Object Hook | Offsets `0x2E` / `0x30` | Seen as `OBJLOCK(*(undefined2 *)(iVar2 + 0x2e)...)`. Matches the properties of live text object frames. |

---

## 8. Decompiled logic of the Master Record Reader

The shape of `FUN_1048_18c4` shows how ToolBook moves from a static file to runtime objects:

```c
// Phase 1: load context and open file handles
iVar2 = *(int *)(unaff_BP + 6);   // base structure / engine context
uVar1 = OBJFILEOPEN(..., iVar2, ..., *(undefined2 *)(unaff_BP + 8));

// Phase 2: lock the stream memory segment to extract properties
lVar6 = OBJLOCK(*(undefined2 *)(iVar2 + 0x80), *(undefined2 *)(iVar2 + 0x82), ...);

// Phase 3: length-bounds check on the raw data stream
iVar2 = FUN_10c8_00de((int)lVar6, *(undefined2 *)(unaff_BP + -2), ...);

// Phase 4: secondary structure lock for 0x76 text / live objects
uVar5 = OBJLOCK(*(undefined2 *)(iVar2 + 0x2e), *(undefined2 *)(iVar2 + 0x30), ...);
```

### 8.1 Phase by phase
- **Phase 1.** The context structure pointer is read from `unaff_BP + 6`. The file is opened through `OBJFILEOPEN`.
- **Phase 2.** The global memory block for the open stream is locked through `OBJLOCK`, using the handle pair at `+0x80` / `+0x82`.
- **Phase 3.** The locked buffer is passed to `FUN_10c8_00de`, which validates length boundaries before any data is copied into the memory layout.
- **Phase 4.** A second `OBJLOCK` through the pair at `+0x2E` / `+0x30` reaches the sub-stream where text-property frames and `0x76` live objects are handled.

The session summary adds that the reader also "freezes execution memory pools" and "steers data tracking frames" while the stream is open.

---

## 9. Ghidra decompiler recovery matrix

`unaff_BP` appears because Ghidra is fighting Watcom's register-heavy convention. When the analysis cache does not refresh, use this table to translate by hand:

| Decompiler element | Counterpart | Function |
| :--- | :--- | :--- |
| `unaff_BP + 6` | Context structure pointer | Tracks file positions, active modules, and dynamic state objects. |
| `iVar2 + 0x80` / `0x82` | Raw data stream handles | Global memory segment block of the open file stream. |
| `FUN_10c8_00de` | `14 00 00` length parser | Unpacks length-prefixed bytes from headers before memory layout copies. |
| `iVar2 + 0x2E` / `0x30` | `0x76` live object array | Pointers for fields, text blocks, and runtime assets. |
| `unaff_BP + 8` | Argument passed to `OBJFILEOPEN` | Fourth argument of the open call. |
| `unaff_BP + -2` | Local passed to the length parser | Second argument of `FUN_10c8_00de`. |

---

## 10. Phase 5: Fixing Ghidra's auto-analysis pipeline

### 10.1 The patch
Edit `Ghidra/Processors/x86/data/languages/x86win.cspec` (the session summary also names `x8616.cspec`). Replace the `<default_proto>` element and define a `__watcall` prototype:

```xml
<prototype name="__watcall" factory="default">
  <input>
    <pentry minsize="1" maxsize="2"><register name="AX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="DX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="BX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="CX"/></pentry>
  </input>
</prototype>
```

### 10.2 Applying it
1. Save the specification file.
2. Terminate hanging Ghidra Java workers so the cache clears:
   - Linux / macOS: `pkill -f ghidra`
   - Windows: `taskkill /F /IM javaw.exe`
3. Restart Ghidra and open the program.
4. Run **Analysis -> Auto Analyze**.

Expected result: the fragmented helper nodes merge back into unified, readable C, and the `unaff_BP` paths go away.

### 10.3 Caveats
- The sources note that Ghidra's cache can keep showing broken stack output even after changes. Hence the manual matrix in section 9.
- The prototype above is exactly as given in the sources. It only lists four register slots and has no `<output>` or `<unaffected>` block. Section 14 covers this.

---

## 11. WDW debugger syntax reference

| Command | Meaning |
| :--- | :--- |
| `bc *` | Clear all breakpoints. |
| `b <module>@<symbol>` | Plain breakpoint on an exported symbol. |
| `b <module>@<symbol> { log "text"; go }` | Log a message, then resume. |
| ALT+6 | Open the WDW Log Window. |

Breakpoints used:

| Symbol | Purpose | Action |
| :--- | :--- | :--- |
| `CDBFILEOPEN` | Entry anchor | Stop. |
| `CDBCREATEPAGEREF` | Page reference creation | Log `Hit PageRef`, continue. |
| `CDBSETVALUEEX` | Value set | Log `Hit SetValue`, continue. |
| `OBJFILEOPEN` | Low-level file open | Log `Hit ObjOpen`, continue. When used for stack capture, set it as a plain stop instead. |
| `CDBPAINTCLIENT` | Exit anchor | Stop. |

---

## 12. Step-by-step reproduction guide

1. Start 86Box 6.0 with a guest that runs the ToolBook runtime. Attach WDW to the process.
2. Run `bc *` to clear old breakpoints.
3. Set the breakpoints from section 11.
4. Open a `.TBK` file. The sample was `C:\TBK\9E54D01.TBK`.
5. When `OBJFILEOPEN` stops at `35A7:177F` on `enter 025A, 00`, record the registers and the stack at `SP`.
6. Read the far return address from the top of the stack. Offset `21AD`, selector `2A4F`.
7. Dump the string pool near `0x93E4` to confirm the file path.
8. Disassemble at `2A4F:219C` through `21C0` and confirm the `cmp byte ptr ss:[bx], 09`.
9. In Ghidra, apply the `__watcall` patch, clear the cache, restart, and re-run Auto Analyze.
10. Locate `FUN_1048_18c4` and `FUN_10c8_00de`, and compare with sections 7 to 9.
11. Remember that segment selectors differ between sessions. Match by structure and offsets rather than raw selector values.

---

## 13. Glossary

- **TBK:** ToolBook book file.
- **Watcom calling convention:** register-based parameter passing (`AX`, `DX`, `BX`, `CX`).
- **`.cspec`:** Ghidra compiler specification file defining calling conventions.
- **`unaff_BP`:** Ghidra's name for a base pointer it could not tie to a known frame.
- **`OBJLOCK`:** locks a global memory object for access.
- **`GLOBALUNLOCK`:** Windows API that releases a locked global memory block.
- **Far call / far return:** call that carries a segment selector as well as an offset.
- **Stream walker:** the unexported routine that iterates records in a `.TBK` stream.
- **`14 00 00` block:** length-prefixed structure whose header the length parser validates.
- **`0x76` object:** live runtime object, such as a text property frame.
- **WDW:** Open Watcom Windowed Debugger.
- **86Box:** x86 hardware emulator.

---

## 14. Discrepancies, gaps, and open items

1. **Missing patch body in the manual.** The Engineering Manual says to define `__watcall` "exactly like this" but the XML block is absent from the PDF. The block in section 10 comes from the Session Summary PDF.
2. **Two spec filenames.** The manual names `x86win.cspec` and `x8616.cspec`. The summary names only `x86win.cspec`. Which file applies depends on the Ghidra version and the language ID used for this binary. This was not resolved in the sources.
3. **Patch completeness.** The prototype lists only input registers. Real Watcom conventions also define return registers and preserved registers. The sources do not say whether this was needed.
4. **Offset caveat.** `0x2E` / `0x30` and `0x80` / `0x82` are structure offsets from `iVar2`. The sources do not name the structure.
5. **Meaning of `0x09`.** Sources describe it as a property type signature that separates length-prefixed targets from standard text streams. The full set of type values was not mapped.
6. **Four pushed arguments.** The manual labels them as file path, mode flags, workspace handle and length boundary. These are interpretations from the setup code, not confirmed by symbols.
7. **Report vs. manual wording.** The report calls the live hook "secondary sub-stream memory structures". The summary calls it the instantiator of active property records. Both describe the same offsets.
8. **Selector values.** Selectors such as `2A4F`, `35A7` and `4857` come from one emulator run and will likely differ in other runs.
9. **Call site for the length parser.** `3FAF:25C4` (`call near ptr 0x0BDC`) is the only call site recorded. Others may exist.

---

## 15. Suggested next steps

1. Define the context structure in Ghidra, with fields at `+0x2E`, `+0x30`, `+0x80` and `+0x82`, and apply it to `FUN_1048_18c4`.
2. Rename `FUN_1048_18c4`, `FUN_10c8_00de` and the `2A4F:21AD` caller inside the Ghidra project.
3. Trace the `0x09` branch at `21C3` and the fallback at `23A8` to document both parsers.
4. Log the bytes the `14 00 00` parser consumes for several `.TBK` files and write down the block layout.
5. Follow the second `OBJLOCK` (`+0x2E` / `+0x30`) to see how `0x76` records are built.
6. Add `GLOBALUNLOCK` to the breakpoint set to confirm frame release order.
7. Test the `__watcall` patch with output and unaffected-register definitions and compare the decompilation quality.
8. Script the WDW session so the capture in section 12 can be repeated with one command file.
