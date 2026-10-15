# 12. The book-open spine

## 12.1 The frames that repeat

On the 2026-10-15 book-open and page walk, these frames were in nearly every WDW Calls window. Selectors are that boot only.

| Selector:offset | Note |
|---|---|
| `3497:03EF` | Early frame. |
| `3497:4A6E` | The planned step point. |
| `3197:0379` | |
| `3167:0CB1` | Near call. |
| `3167:14BC` | Far call. |
| `3247:02BF` | Near. |
| `3247:05B7` | Near. |
| `3247:0B7A` | Far. |

Everything else in those captures hangs off this spine. The full selector-to-decompile table for that boot is `maps/wdw-to-ghidra.md` (485 lines). It is a lookup, not a finding. Do not treat a selector from that file as valid on the next boot.

## 12.2 What the three export traces contained

WDW has no full call trace. `break <symbol> resume on` plus `log <file>` logs named exports and continues. `resume on` is a property of a breakpoint that already exists. Module qualification is `TB80BAS@OBJFILEOPEN`. SoftICE `!` does not work in WDW.

| Trace | Shots | What fired | What did not |
|---|---|---|---|
| W16 | 11 | `GETPLATFORMREF`, `IS32BITENV`, `GETRUNTIMELOCALIZEDDLL`, `ACXINITIALIZETOOLBOOKSUPPORT`, `ACXOLEINITIALIZE`, `ASYM_STRINGFROMCLSID`, `SETTHUNKINGLAYERSERRORFUNC`, `LOADLIBRARYEX32W`, `GETPROCADDRESS32W` | Book open. Record walk. |
| UTL | 53 | `GETCHARINFO`, `GETSTRMGRSTRING`, task collections, `PLUGINSVCINIT`, `LOADRESSTR`, `CXTHELPINIT`, `GETTBKINIPROFILEINT` / `STRING`, `INITMETRICS`, `SETCONVERSIONDC`, `CXTTOPXT`, `GHEAPCREATE`, `GHEAPALLOC`, `SYMLOOKUPNUMBER` | Record walk. The type-name table lives here and was not the thing being stepped. |
| BAS | 173 | `VALUETOSTRING`, `VALUENEWSTACK`, the `VALUENEW*` family, `OBJFILEOPEN` (`enter 025A`), `STACKGETSIZE`, `STACKPUSH`, `CDBCHUNKLAST`, `CDBCHUNKFIND`, `CDBCHUNKEND`, `RESMGR*` | A compare of a far pointer to `0x14`. Ordinal 51. |

`OBJFILEOPEN` in that BAS trace is the file-open path. The buffered reader is `FUN_1160_03de`, reached through `FUN_1258_00a8`. When the buffer satisfies the request, the raw DOS path at offset `04F3` is skipped. Live 4-byte reads returned an internal pointer (`FC B5 BD B0` in one dump), not a page header and not `03 4A 42 4F`.

## 12.3 Where to break next

1. `TB80BAS@CDBFILEOPEN` on a lesson open. Resume.
2. Then `CDBCREATEPAGEREF` or `CDBSETVALUEEX` (export names, not the selectors above).
3. When an object exists, dump `+0x0F` and the page offset it came from. That pair names the reader.
4. Do not break ordinal 51. Do not schedule another pass over the same W16 and UTL exports in order to find the reader.

The reader is still unnamed. The working model is in chapter 4: a length-prefixed walk in BAS after `CDBFILEOPEN` and before the first paint, with no literal `14 00 00` compare required.

## 12.4 Debugger facts that keep wasting a session

SoftICE field work closed 11 October 2026 (`SI405w9x` plus ICEDUMP 6.021). Ordinal breakpoints survive a reboot. Selectors do not. `TB80BAS.Ordinal_8` is `CDBFILEOPEN` on every boot.

`/DUMP` writes the SoftICE console unless the dump experts are set. Several early `page.bin` and `rtm.bin` files are command logs or the DOS device chain (`CON`, `AUX`, `PRN`). A dump is real when it contains book strings at offsets already known, as `page.bin01511` did (`ASYM_TpID`, `Page#`, matching `9e954d01.tbk` at `0xB8B51`).

Symbol maps are `NE-segment:offset` names (`TB80BAS.map`, 3799 entries; `TB80RTM.map`, 2669). SoftICE and WDW do not load a `.map` as a module.

The CMP expand host died in `TB80W16` at `001c:00000015` (`9A 9C 06 57 2A`, segment not present). That fault is parked. It is not the book-open path.

The Unicorn host has not opened a book. Passes 01–07 fill segments and bind 461 ToolBook ordinals, then die at `FFFF:0158` and `0080:0098`. Pass 06 exits after `TB80.INI`. The three hosts (the RTM experiment, `newl`, `neww`) are not one program.
