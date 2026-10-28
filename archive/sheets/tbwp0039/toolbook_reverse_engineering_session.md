# ToolBook Binary Reverse Engineering Session Log

**Target Framework:** Legacy 16-bit ToolBook Engine (`TB80BAS.DLL` / `TB80RUN.EXE`)  
**Session Focus:** Isolating the stream walker, data-block parser, and runtime hooks.

---

## 1. Primary Architectural Findings

| Component Name | Ghidra Target ID | Operational Functionality |
| :--- | :--- | :--- |
| **Master Record Reader** | `FUN_1048_18c4` | Handles high-level lifetime hooks, file loading loops, and object memory descriptors. |
| **14 00 00 Length Parser** | `FUN_10c8_00de` | Low-level block parser reading length-prefixed bytes directly out of the stream buffer. |
| **0x76 Live Object Hook** | Internal Offsets `0x2E` / `0x30` | Tracks active instantiation of runtime properties and layout states prior to window drawing. |

---

## 2. Live Debugger Trace & Context Identification

Through real-time emulation inside **86Box**, a breakpoint hit at `OBJFILEOPEN` (`35A7:177F`) captured the caller register environment state immediately prior to stack pointer execution:
* **Caller Entry Pointer:** Located safely at segment selector offset **`2A4F:21AD`**.
* **Memory Data Segment String:** Extracted string pointing directly to `C:\TBK\9E54D01.TBK`.
* **Structural Condition Validation:** Post-return code at `21B7` processes validation checks via `cmp byte ptr ss:[bx], 09`.

---

## 3. 16-Bit Watcom C Calling Convention Correction

The standard Ghidra decompiler suffers from layout fragmentation due to unrecognized register parameter layouts (arguments pushed in `AX`, `DX`, `BX`, `CX`). Globally adjusting the `.cspec` default calling convention selector signature strips out broken `unaff_BP` tracking paths and forces continuous control flow merging.

### Watcom Debugger (WDW) Corrected Breakpoint Script Syntax:

```text
bc *
b TB80BAS@CDBFILEOPEN
b TB80BAS@CDBCREATEPAGEREF { log "Hit PageRef"; go }
b TB80BAS@CDBSETVALUEEX { log "Hit SetValue"; go }
b TB80BAS@OBJFILEOPEN { log "Hit ObjOpen"; go }
b TB80BAS@CDBPAINTCLIENT
```
