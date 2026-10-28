# TB80W16 — WDW trace (partial)

> Trail, 2026-10-16. Chapter 12. 11 W16 shots. No book open. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-15  
**Source:** W16-partial-2.zip (11 screenshots)  
**Debugger:** Open Watcom Debugger on Win98  

This is a partial trace of TB80W16 initialization after RTM has started. The screenshots step through platform detection, OLE init, and the 32-bit thunk layer setup.

---

## Screenshot 21-21-49

- **Module:** TB80RTM
- **Address:** 3C3F:0362
- **Instruction:** `or ax,ax` (after `call far ptr INITTASK`)
- **Break on:** XDLLTRANSWINPROC
- **Notes:** Still in RTM. Just returned from INITTASK. The W16 load has not yet been stepped into. Functions window shows W16 exports (ASCIIFILEDLGHOOKPROC, ASYM_ASCIIFILEDLGHOOK, etc.).

## Screenshot 21-26-56

- **Module:** TB80W16
- **Address:** 3FFF:0158
- **Function:** GETPLATFORMREF
- **Prolog:** `mov ax,3D37` / `enter 0014,00`
- **Break on:** GETPLATFORMREF
- **Calls window:** shows prior frames including 2A47:03EF, 2A47:4A6E, and two ??? entries.
- **Notes:** First W16 function hit. Sets up a frame and calls a near pointer at 0000 (likely a platform query).

## Screenshot 21-27-04

- **Module:** TB80W16
- **Address:** 400F:05B2
- **Function:** GETRUNTIMELOCALIZEDDLL
- **Prolog:** `mov ax,3D37` / `enter 000E,00`
- **Break on:** GETRUNTIMELOCALIZEDDLL
- **Notes:** Looks up the runtime localized DLL. Calls near ptr 0092, then checks AX. Functions list shows GETPLATFORMREF, GETPROCADDRESS32W, GETRUNTIMELOCALIZEDDLL, GETTHUNKINGLAYERSERRORFUNC.

## Screenshot 21-27-15

- **Module:** TB80W16
- **Address:** 3F27:021A
- **Function:** ASYM_IS32BITENV
- **Prolog:** `mov ax,3D37` / `push bp` / `mov bp,sp`
- **Break on:** ASYM_IS32BITENV
- **Notes:** Wrapper. Calls far ptr IS32BITENV, then leave/retf. Functions window shows ASYM_* helpers (ASYM_MAKEPATH, ASYM_CGETCWD, ASYM_CLSIDFROMPROGID, etc.).

## Screenshot 21-27-25

- **Module:** TB80W16
- **Address:** 3FFF:0172
- **Function:** IS32BITENV
- **Prolog:** `mov ax,3D37` / `enter 0014,00`
- **Break on:** IS32BITENV
- **Notes:** The actual check. Sets up frame, calls near ptr 0000. Returns whether the environment is 32-bit.

## Screenshot 21-27-42

- **Module:** TB80W16
- **Address:** 4027:0E24
- **Function:** ACXINITIALIZETOOLBOOKSUPPORT
- **Prolog:** `mov ax,3D37` / `enter 0010,00`
- **Break on:** ACXINITIALIZETOOLBOOKSUPPORT
- **Notes:** ActiveX/ToolBook support init. Moves 0014 into AX, stores into [bp-10], then calls far ptr ?GETDATA@TASKCOLLEC. Functions window shows ACX* entries (ACXCTBKSIMPLEOLEDISPATCH, ACXINIT, ACXOLEINITIALIZE, ACXSTARTUP).

## Screenshot 21-27-49

- **Module:** TB80W16
- **Address:** 4027:11C0
- **Function:** ACXOLEINITIALIZE
- **Prolog:** `mov ax,3D37` / `enter 000A,00`
- **Break on:** ACXOLEINITIALIZE
- **Notes:** OLE init. Calls near ptr 0F14, then near ptr 0DD2. Functions window still on ACX* list.

## Screenshot 21-28-03

- **Module:** TB80W16
- **Address:** 3F57:0584
- **Function:** ASYM_STRINGFROMCLSID
- **Prolog:** `mov ax,3D37` / `push bp` / `mov bp,sp`
- **Break on:** ASYM_STRINGFROMCLSID
- **Notes:** CLSID to string. Compares word ptr 06[bp] against 0027, jumps if above. Functions window shows ASYM_OPENFILE, ASYM_OPENFILEEX, ASYM_STRINGFROMCLSID, ASYM_URLDOWNLOAD, ASYM_XFORM* entries.

## Screenshot 21-28-17

- **Module:** TB80W16
- **Address:** 4047:0316
- **Function:** SETTHUNKINGLAYERSERRORFUNC
- **Prolog:** `mov ax,3D37` / `push bp` / `mov bp,sp`
- **Break on:** SETTHUNKINGLAYERSERRORFUNC
- **Notes:** Sets the error function for the thunk layer. Pushes arguments and calls near ptr 0CB2. Functions window shows GETVDMPOINTER32W, IS32BITENV, ISCOMMONDLGLAUNCHED, LOADLIBRARYEX32W, MINIMIZETHUNKINGLAYERS.

## Screenshot 21-28-24

- **Module:** TB80W16
- **Address:** 4087:0262
- **Function:** LOADLIBRARYEX32W
- **Prolog:** `mov ax,3D37` / `enter 0010,00`
- **Break on:** LOADLIBRARYEX32W
- **Notes:** 32-bit LoadLibraryEx thunk. Calls far ptr 4047:04EE. Functions window shows LOADLIBRARYEX32W, LOADLOCALIZEDSTRING, MINIMIZETHUNKINGLAYERS, OPENFILE32W.

## Screenshot 21-28-35

- **Module:** TB80W16
- **Address:** 4087:02EA
- **Function:** GETPROCADDRESS32W
- **Prolog:** `mov ax,3D37` / `enter 0010,00`
- **Break on:** GETPROCADDRESS32W
- **Notes:** 32-bit GetProcAddress thunk. Calls far ptr 4047:04EE. Functions window shows COMPILERCOMPILETEXT, CREATEDIBMASK32, GETPROCADDRESS32W, GETRUNTIMELOCALIZEDDLL.

---

## Summary

The partial W16 trace covers:

1. Platform detection (GETPLATFORMREF, IS32BITENV)
2. Runtime localized DLL lookup
3. ActiveX/OLE initialization (ACXINITIALIZETOOLBOOKSUPPORT, ACXOLEINITIALIZE)
4. CLSID string conversion
5. Thunk layer error function setup
6. 32-bit LoadLibraryEx / GetProcAddress thunks

W16 is the command bus and thunk layer. These functions set up the 32-bit bridge and OLE support. They are not on the book-open or record-reader path.
