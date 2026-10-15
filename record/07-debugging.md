# 7. Debugging and hosts

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| D-001 | Known | SoftICE and the Watcom debugger do not share command syntax. SoftICE field work closed 11 October 2026. Later breaks are WDW. | field manual, `tbwp0026/wdw-break-syntax.md` |
| D-002 | Known | WDW has no full automatic call trace. `break <symbol> resume on` plus `log <file>` logs and continues. `resume on` is a property of a breakpoint that already exists. | `tbwp0026/wdw-trace.md` |
| D-003 | Known | In WDW, module qualification uses `@` (`TB80BAS@OBJFILEOPEN`). SoftICE’s `!` does not work there. | same note |
| D-004 | Known | Symbol maps are `NE-segment:offset name`. The segment index is not a live selector. SoftICE and WDW do not load the `.map` as a module. | `tbwp0003/TB80BAS.map` (3799 entries), `TB80RTM.map` (2669) |
| D-005 | Known | The Unicorn host has not opened a lesson. Pass 06 exits after `TB80.INI`. The entry does not ask for the book. | WV-006, WV-036 |
| D-006 | Known | TBCBT NE segment 7 holds `KEYEDPASSWORDENCRYPTEX`, `MAKEKEYEDPASSWORDEX`, `ENCRYPTEX`, and `DECRYPTEX`. | WV-043 |
| D-007 | Known | NE segment numbers are not Ghidra’s `CodeN` names. Segment 1 is `1000`, segment 2 is `1008`, and the usual step is 8, with gaps. | `TBdecompile/maps/rtm-ne-to-ghidra.md` |

## 7.1 SoftICE

The kit is `SI405w9x.exe` plus ICEDUMP 6.021. The loader that worked was `w9x/4.05.334/icedump.exe`. It loaded on the Windows 98 VM after both `kernel32.dll` and `user32.dll` exports were listed in `winice.dat`.

Ordinal breakpoints are stable across boots. Selectors are not. `TB80BAS.Ordinal_8` is `CDBFILEOPEN` on every boot. `36F7:03DE` is `FUN_1160_03de` only until the next reboot.

`/DUMP` writes the SoftICE console, not the address given, unless the dump experts are set. Several early `page.bin` and `rtm.bin` files are command logs or the DOS device chain (`CON`, `AUX`, `PRN`). A dump is real when it contains book strings at the file offsets already known, as `page.bin01511` did (`ASYM_TpID`, `Page#`, matching `9e954d01.tbk` at `0xB8B51`).

Do not mix these commands into a WDW session.

## 7.2 WDW

On the Watcom debugger:

- Create the breakpoint first, then set `resume on`.
- Qualify with `@`, not `!`.
- Log with `log <file>`.
- There is no trace that prints every call. The three logs in `tbwp0026` are named-export hits: 11 in W16, 53 in UTL, 173 in BAS.

Those three logs are described in chapter 4. They do not contain the reader. The next useful break is after `CDBFILEOPEN`, on the lesson path, not another pass over the same exports.

GPF notes from the SoftICE sessions still apply in spirit: do not step into an unloaded segment, and do not single-step a far call into `KERNEL` unless that segment is present. The CMP expand host died in `TB80W16` at `001c:00000015` (`9A 9C 06 57 2A`, segment not present). That fault is parked. It is not the book-open path.

## 7.3 Unicorn

`unfold.py` enters 16-bit protected mode, calls `BootApp`, and dumps each segment `LoadAppSeg` materializes. Pass 01 filled 3 of 139 RTM segments. Pass 02 filled 138, after the call stub was flushed from the Unicorn cache so every call did not replay segment 2. Passes 03 through 07 bind imports, including 461 ToolBook ordinals to real DLL segments. 339 imports stay Windows stubs. The host still dies at `FFFF:0158` and `0080:0098` before a DOS open of the book.

**Thought (WV-008).** A real Win16 return is what would get that host further. The three hosts (the RTM experiment, `newl`, `neww`) are not one program and do not share a Windows table (WV-035).

The path that does open a page is the pipeline host, which parses the file instead of running RTM. On `9e954d01.tbk` that open is at `0x9EC`, 129 pages. `render.html` is written only when the debug-render flag is set (WV-034).

## 7.4 Password cipher

`TBCBT` segment 7 (Ghidra `Code7`, base `1030`) holds the four cipher exports. A SoftICE module list that showed segments `01`, `0E`, `02`, `0B`, `08`, `0D`, `04`, `03` had not loaded segment 7. The dialog is an ordinary Windows dialog. The cipher is not in the dialog procedure.

After a failed password, the typed string and the constants `0xA01` and `0x300` remain in memory. Searching for those constants finds the call site even while segment 7 is unloaded. The three addition schemes, the with-password file delta, and the fact that the stand-in key does not decrypt it are chapter 16. The NIDA `.sbk` passwords are not recorded here. They are not required to read the decompile.

## 7.5 Ghidra

Two NE loader bugs were fixed for this work: the entry-table segment byte was treated as signed, and `ne_cbenttab` was ignored. `TB80BAS` is the image with entry segment bytes at or above 128. The unpacker does not rewrite those bytes. The Ghidra patch does. An honest BAS image loads in the patched Ghidra 12.1.4 build.

Force-disassemble scripts recover functions the loader never reached. One walks undefined `C8` (`ENTER`) bytes. The next accepts a real `RET` / `RETF` before treating the following byte as code, and it only creates functions at entry-like symbols. Run `C8` first, then the prologue pass. They do not name anything, and they do not touch code that is already defined.

`SENDMESSAGE` (321 hits in one RTM listing) and `LSTRLEN` (282 hits) have mangled arguments. That is a decompiler problem, not a missing function. It wants a fresh decompile, not another reading of the same HTML.
