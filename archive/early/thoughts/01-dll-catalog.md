# ToolBook II 8.1 DLL and Module Catalog

**Date:** 2026-10-11  
**Source:** Version resources and export names from the unpacked NE images and the PE modules in `binaries/`.

Roles are grounded in the binaries, not just the filenames. NE modules were Optloader-packed; export names below come from the unpacked images.

## Process and thunk

| Module | Role |
|--------|------|
| `tbload.exe` | Course opener. Reads the Click2learn shell, starts the runtime. |
| `TB80MAIN.EXE` | Small PE stub on the runtime side of startup. |
| `TB80RUN.EXE` | 32-bit launcher. Exports only mutex wait/release. |
| `TB80RTM.EXE` | 16-bit shell. Main window, print, DDE, find, history, status bar, resource picker. Window classes include `EGYPT*`. |
| `TB80W32.DLL` | 32-bit half. `TBXInstance`, `MEM1632`, DIB dither, language id. ~246 exports. |
| `TB80W16.DLL` | 16-bit half. `CallProc32W`, `WowHandle*`, file thunks, palette and graphic entry points. ~406 exports. |
| `TB80F32L.dll` | Flat 32-bit entry (`F32EntryAPI`, `zCDHookProc`). Common-dialog hook side. |
| `TBFILE32.DLL` | Long-name support for the 16-bit engine. |
| `TB80NET.EXE` | Network access provider. 16-bit NE executable, not a DLL. |

## Book engine

| Module | Role |
|--------|------|
| `TB80BAS.DLL` | Server. 606 exports, the `CDB*` API: init, open, save, merge, view page, view background, selection. Descendant of 1.5 `TBKBASE`. FileDescription: “ToolBook Server DLL”. |
| `TB80CMP.DLL` | OpenScript. `COMPILERCOMPILETEXT`, `COMPILEREXPANDTEXT`, `CFUNEXECUTE`, `CFUNEVALUATE`, debugger entry from P-code offset. Keyword resources 0x77/0x78. FileDescription: “ToolBook Compiler DLL”. |
| `TB80UTL.DLL` | Utilities and object classification table (Page, Button, Field, Polygon, …). |
| `TB80RCR.DLL` | Linked by `TB80RTM` next to the book server. Resource side of the runtime; exports not fully annotated. |
| `TB80ENU1.DLL` | 16-bit English string table. `LoadLocalizedString`, named-string index. |
| `TB80ENU2.DLL` | 32-bit copy of the same localization exports. |

## Drawing and media

| Module | Role |
|--------|------|
| `TB80BMP.DLL` | Graphic display, metafile play, FX bitblt. FileDescription: “ToolBook graphic display”. |
| `TB80JPG.DLL` | JPEG. Version resource still says original name `TB60JPG.DLL`. |
| `TB80FLT.DLL` | Filter and clip editor. Media path lists, clip notify. FileDescription: “ToolBook Filter DLL”. |
| `TB80LNL.DLL` | Multimedia ToolBook media engine. Lionel callbacks. FileDescription: “Multimedia ToolBook Media Engine”. |
| `TB80MM.DLL` | Multimedia notification only. Small. |

## OLE, ActiveX, old VB

| Module | Role |
|--------|------|
| `TB80OLE.DLL` | OLE data object, clipboard, automation dispatch. |
| `TB80OCX.DLL` | 16-bit OLE control support. |
| `TB80ACX.DLL` | 32-bit ActiveX site. `TBXOCXSite` / `TBXOleSite` get/set/send. |
| `TB80VBX.DLL` | VBX support, already legacy in 2001. |
| `TB80RMT.DLL` | Remote/automation peer. PE; not unpacked with the NE set. |

## OpenScript `linkDLL` libraries

These are the extension commands a script links by name. They are not on the open path unless a handler calls them.

| Module | Role |
|--------|------|
| `TBDLG.DLL` | Common dialogs. |
| `TBWIN.DLL` | Display metrics, `WIN.INI`, page/client coordinate conversion. |
| `TBDOS.DLL` | DOS file and directory calls. |
| `TBREG.DLL` | Registry get/set/list. |
| `TBDB3.DLL` | dBase III navigation and indexes. |
| `TBPDX.DLL` | Paradox tables, keys, passwords. |
| `TBCBT.DLL` | CBT scoring and question helpers. FileDescription: “ToolBook CBT Extension DLL”. |

## System books (the other half of the product)

| Book | Role |
|------|------|
| `tb80r.sbk` | Reader runtime script (~953 KB). Menu, navigation, status behavior that is not in `TB80RTM`. |
| `tb80hyp.sbk` | Hyperlink / help behavior. |
| `tb80anm.sbk` | Path animation. |
| `nc81base.sbk`, `nc81test.sbk`, `nc81recs.sbk`, `nc81trnr.sbk` | NIDA lesson shell: base, test, records, trainer. |
| `nc81int.dll`, `nc81rec.dll` | Course-specific interop and record store, not Asymetrix. |

`linkDLL` and system books are the two extension mechanisms Asymetrix documented: a system book adds a script above the book; a DLL adds commands. Most of what authors think of as ToolBook is one of those two, not `TB80BAS`.

## Notable export landmarks

- `TB80BAS`: `CDBINIT` (1), `CDBFILEOPEN` (8), `CDBFILESAVE` (9), `CDBVIEWPAGE` (15), `CDBVIEWBKGND` (18).
- `TB80CMP`: `COMPILERCOMPILETEXT` (1), `COMPILEREXPANDTEXT` (3), `CFUNEXECUTE` (8), `CFUNEVALUATE` (9).
- `TB80RTM`: `MAINWNDPROC`, `EGYPTCLIENTWNDPROC`, `STATUSBARWNDPROC`, plus a long list of dialog procs (print, find, history, font, etc.).

## What is still thin

- Full annotation of `TB80RCR` exports.
- Whether `TB80RMT` is required for the lesson path (it is not referenced by the course opener).
- Exact mapping from `TB80UTL` classification table indices to the on-disk kind bytes inside `14 00 00` chunks.
