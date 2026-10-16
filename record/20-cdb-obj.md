# 20. CDB and OBJ

**Date:** 2026-10-16

**Status:** The split between the `CDB*` and `OBJ*` exports of `TB80BAS`. Counts are the NE export table of the unpacked DLL (606 named entries). Call sites are `TB80BAS.DLL.c`. Relocation counts are the unpacked images. This does not name the record reader.

## Claims

| Id | Grade | Statement |
|---|---|---|
| S-001 | Known | Ordinals 1 through 56 are `CDB*`, with no other name in between. Ordinal 57 is `LOCKPATTERN`. There are 128 `CDB*` exports in all, across 26 NE segments. |
| S-002 | Known | There are 29 `OBJ*` exports. Twenty-six of them are NE segment 47 (Ghidra `1170`). `OBJARENACHECK` is segment 44, `OBJEXPORTMSGNEAR` is 49, `OBJINIT` is 103. `OBJECTNAME` (ordinal 160, segment 61) is not one of them. |
| S-003 | Not true | "`CDB*` is the header and `OBJ*` is the definition of the same functions." Both are exported functions with bodies. Three stems occur on both sides (`INIT`, `FILEOPEN`, `FILECLOSE`). Those are not the same function. |
| S-004 | Known | `CDBGETVALUE`, `CDBSETVALUE`, and `CDBSENDVALUE` are one call each, into the matching `*EX` export, with `0` in the extra argument. `CDBUNREGISTEROLE2WINDOW` is `CDBREGISTEROLE2WINDOW(0, 0, ...)`. |
| S-005 | Known | `CDBGETVALUEEX` locks with `OBJLOCKNEAR`, calls the code pointer at the `0x76` slot, then `OBJUNLOCK`. The same three calls (`lock near`, the operation, `unlock`) are in `CDBSETVALUEEX` and `CDBSENDVALUEEX`. |
| S-006 | Known | `CDBFILEOPEN` does not name `OBJFILEOPEN`. The decompile reaches it through `FUN_1048_1cc4` and through `FUN_1030_02fc`. Those two call `FUN_1048_1766` and `FUN_1048_2174`, and those call `OBJFILEOPEN`. |
| S-007 | Known | Outside BAS, the modules whose import table names `TB80BAS` are RTM, CMP, NET, and FLT. RTM's BAS relocations are `CDB*`, `VALUE*`, `STACK*`, `HEAP*` / `TBHEAP*`, and `RESMGR*`. The only `OBJ*` name among them is `OBJBOOKVERSION`. |
| S-008 | Thought | `CDB*` is the book API the other modules link. `OBJ*` is the object file and the object memory inside BAS. The DLL never expands the letters. The C++ objects are the mangled `TBX*` classes, which are a third layer. |

## 20.1 Not a header and a C file

A header would declare a function whose body lived in one object file. That is not this split.

The DLL contains no `.c` or `.h` names. Copyright string: Asymetrix, 1990–1995. Both prefixes are in the resident and nonresident name tables, so both are linkable. `CDBGETVALUE` is one call, and the function it calls is `CDBGETVALUEEX`, not an `OBJ*` function. The short-name / `EX`-name pair is inside `CDB*`.

`CDBINIT` (line 30304) is 193 lines of device caps, pens, and colors. At line 30465 it calls `OBJINIT(0x242, 7, param_1)` and returns if the error byte was set. `OBJINIT` (line 142908, NE segment 103) runs once: a profile int via `GETTBKINIPROFILEINT`, then `FUN_11a8_0000`. The book init starts the object layer. It is not a prototype for it.

The three shared stems:

| Stem | Book side | Object side | What the decompile shows |
|---|---|---|---|
| `INIT` | `CDBINIT`, ordinal 1 | `OBJINIT`, ordinal 225 | One call, above. |
| `FILEOPEN` | `CDBFILEOPEN`, ordinal 8, line 27592 | `OBJFILEOPEN`, ordinal 227, line 76162 | Not a direct call. Section 20.3. |
| `FILECLOSE` | `CDBFILECLOSE`, ordinal 11 | `OBJFILECLOSE`, ordinal 246 | `CDBFILECLOSE` does not call it. `CDBFILESAVEAS` does, once, and also calls `OBJFILECOPY`. |

`CDBFILENEW` calls `OBJLOCK`, `OBJTOUCH`, and `OBJUNLOCK`. `CDBSETFOCUS` calls `OBJPRINCIPALOO`. `CDBDELETEOBJECTVALUE` calls `OBJLOCK`, `OBJLOCKNEAR`, `OBJFREENEAR`, and `OBJUNLOCK`. No `OBJ*` body calls a `CDB*` function. `OBJECTNAME` does: `CDBVALUEBOOKTOSTRING` and `CDBSETPLERR`. That export is not in segment 47.

The 2026-10-12 symbol map line `11A8:04F6 OBJFILEOPEN` is `FUN_11a8_04f6`. The decompile calls that `FUN_` by name a few lines above the real `OBJFILEOPEN`. The export offset is `177C`. Chapter 11 already has that offset. Do not use the map line.

## 20.2 What each side is

Ordinals 1 through 56 are the book surface, in order: instance and thread, file, view, paint, the ref constructors (`CDBCREATEBOOKREF`, `CDBCREATEPAGEREF`, `CDBCREATEBKGNDREF`, `CDBCREATEGRAPHICREF`), the value bus, `CDBSENDCREATE` (ordinal 51, still author-only, chapter 4), `CDBNEWOBJECT`, then the four text chunkers. Fonts and patterns start at 57. Later `CDB*` exports exist (`CDBSETPLERR`, the OLE forwards, the break addresses). They are not in that first run.

`OBJ*` in segment 47 is the object machinery:

| Group | Exports |
|---|---|
| Allocate and free | `OBJNEWNEAR`, `OBJNEWNEAREX`, `OBJREALLOCNEAR`, `OBJREALLOCNEAREX`, `OBJFREENEAR`, `OBJFREENEAREX`, `OBJFREE`, `OBJNEWSEG`, `OBJFREESEG`, `OBJTOUCH` |
| Lock | `OBJLOCK`, `OBJUNLOCK`, `OBJLOCKSEG`, `OBJLOCKNEAR` |
| File | `OBJGETFILE`, `OBJGETHDRLONG`, `OBJFILEOPEN`, `OBJFILECLOSE`, `OBJFILECOPY`, `OBJFILETYPE`, `OBJREADFAR`, `OBJBOOKVERSION` |
| Handle and principal | `OBJOOTOOH`, `OBJOPTOOH`, `OBJPRINCIPALOO`, `OBJPRINCIPALOP` |

`OBJNEWNEAR` (line 75226) is a body, not a macro: `FUN_1258_001c`, then `FUN_1178_0518`. About seventy functions in BAS call it. None of those callers is a `CDB*` export. The book exports lock and free. The unnamed functions allocate.

`CDBGETVALUEEX` (line 38488) is the pattern the value bus uses. The index expression at line 38671 is `(param_7 & 0xff) * 0x76` added to the word at `local_6 + 2`. The code pointer is the dword at `+4` of that slot. `OBJLOCKNEAR` runs, the pointer is called, then `OBJUNLOCK` (line 38690). When the other handle is set, the call is `FUN_1008_03f6` instead, still between the same lock and unlock. `CDBSETVALUEEX` and `CDBSENDVALUEEX` do the same lock. The stride is the live object from chapter 4. This is not a second measurement of the size, and it is not `TBHEAPALLOC`.

`CDROM*` and `CDROMOBJINFO_*` are a different prefix (self-test, drop target, object-info procs). They are not this `OBJ*` segment. `VALUEFROMCDBVALUE` is the converter RTM imports (17 relocation sites). A CDB value and a script `VALUE*` are not the same word. `HEAPFINDCDBVALUE` and the `0xCDBF` argument stay chapter 19. Do not read that tag as one of these exports.

## 20.3 File open

`CDBFILEOPEN` calls `FUN_1030_02fc`, `FUN_1030_0d08`, `FUN_1048_1cc4`, and `FUN_1048_0b46`. It does not mention `OBJ*`.

`FUN_1048_1cc4` (line 29115) is also called by `CDBFILEMERGE` and `CDBCREATEBOOKREF`. Its decompile calls `FUN_1048_2174` and `FUN_1048_1766`. Both of those call `OBJFILEOPEN`. `FUN_1030_02fc`, which `CDBFILEOPEN` also calls, calls `FUN_1048_1766` as well. `FUN_1048_1766` has other callers (`FUN_1028_3adc`, `FUN_1040_0ca8`, `FUN_1048_159a`, several `FUN_1078_*`, `FUN_10c8_144c`). It is a shared file helper, not the open path alone.

Two more callers of `OBJFILEOPEN` sit outside that segment: `FUN_1170_34cc` (inside segment 47) and `FUN_1350_1000`. The bodies of `1cc4`, `1766`, `2174`, `34cc`, and `1000` were not read. The claim is the call graph, not a description of what each one parses.

Chapter 4 stands. `OBJFILEOPEN` is the large file frame (`enter 0x25A` on the boot that stopped there). A 4-byte read on that path was an internal pointer, not a page record. Reaching it from `CDBFILEOPEN` does not make it the reader.

## 20.4 Who links which

Relocation sites against `TB80BAS` in the unpacked images:

| Module | Sites | What they are |
|---|---:|---|
| `TB80RTM.EXE` | 983 | 373 `CDB*` (98 distinct names), plus `VALUE*`, `STACK*`, `HEAP*` / `TBHEAP*`, `RESMGR*`. `OBJECTNAME` is 9 sites. `OBJBOOKVERSION` is 6. No `OBJLOCK`, `OBJNEWNEAR`, `OBJFILEOPEN`, or `OBJUNLOCK`. |
| `TB80CMP.DLL` | 44 | `CDBLOOKUPNUMBER` (2), `CDBSETPLERR`, `CDBGETVALUE`. The rest are `VALUE*` and `HEAP*` / `TBHEAP*`. |
| `TB80NET.EXE` | 1 | `CDBNETCOMINIT`. |
| `TB80FLT.DLL` | 1 | `CONVERTTORUNTIMEMEDIAPATH`. Not `CDB*` or `OBJ*`. |

`TB80W16`, `TB80OCX`, `TB80VBX`, `TB80UTL`, `TB80OLE`, `TB80MAIN`, and `TB80RUN` do not name `TB80BAS` in the module-reference table. The packed originals are the wrong file for this count: every segment but the stub has the relocation flag clear. The unpacked images are the ones with 134 relocating segments in RTM.

One hundred of the 128 `CDB*` names appear in some other module's relocation table. The object manager does not.

## 20.5 The third layer

`TBX*` is 117 exports, starting at ordinal 291 (`TBX32MSGTHUNK`). Some names are the other two prefixes with `TBX` glued on: `TBXCDBGETVALUE`, `TBXCDBSENDVALUE`, `TBXCDBSETPLERR`, `TBXOBJPRINCIPALOO`, `TBXOBJSENDNEAR`, `TBXCURRENTCDBID`, `TBXENUMCDBIDINSTANCES`. Those are still inside BAS. They are not a second DLL.

The C++ objects are the mangled exports: `TBXBASE`, `TBXUSER`, `TBXLAYER`, `TBXOBJECT`, `TBXBOBJ`, `TBX32OBJECT`, `OCXSTUBOBJECT`. Each publishes `SENDPROC`, `GETPROC`, and `SETPROC`. `CDROPTARGET` is the drop target. `CVARIANTVALUEUTILITIES` is the variant bridge. That is the C++ object layer. `OBJ*` is `__stdcall16far` C, not those methods.

`GETCDBID` and `TBXCURRENTCDBID` are exports. The binary does not say what the three letters stand for. Do not expand them.

## 20.6 What this does not change

The reader is still the unnamed walk after `CDBFILEOPEN` and before the first paint. Chapter 4. The next break is still `CDBCREATEPAGEREF` or `CDBSETVALUEEX`.

Not read for this chapter: the bodies of `FUN_1048_1cc4`, `FUN_1048_1766`, `FUN_1048_2174`, `FUN_1170_34cc`, and `FUN_1350_1000`; the principal-op callee; every `CDB*` export after the value bus. `CDBSENDCREATE` was not re-opened.
