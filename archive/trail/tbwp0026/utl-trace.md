# TB80UTL — WDW trace (after INITTASK)

> Trail, 2026-10-16. Chapter 12. 53 UTL shots. No record walk. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-15  
**Source:** UTL after INITTASK-3.zip (53 screenshots)  
**Debugger:** Open Watcom Debugger on Win98  

This is a post-INITTASK trace of TB80UTL. The screenshots step through utility functions: character info, string management, task collection, plugin init, resource loading, help, profile, metrics, heap, and symbol table.

---

## Screenshot 21-43-06

- **Module:** TB80UTL
- **Address:** 3B17:0000
- **Function:** GETCHARINFO
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GETCHARINFO
- **Notes:** Character info lookup. Reads word ptr 0518 into AX, word ptr 051A into DX. Functions window shows GETCHARINFO, GETGDIMETRICS, GETGDISCALE, GETPLUGINDATA, GETPLUGINWINDOW, GETPPIXY, GETSTRMGRSTRING.

## Screenshot 21-43-14

- **Module:** TB80UTL
- **Address:** 3A3F:0122
- **Function:** GETSTRMGRSTRING
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GETSTRMGRSTRING
- **Notes:** String manager string lookup. Subtracts 000C from SP, reads word ptr 06[bp].

## Screenshot 21-43-24

- **Module:** TB80UTL
- **Address:** 3947:0110
- **Function:** ?GETDATA@TASKCOLLECTION@@RECPEXXZ
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** ?GETDATA@TASKCOLLECTION@@RECPEXXZ
- **Notes:** C++ task collection data getter. Functions window shows ??0CVECTOR, ??1TASKCOLLECTION, ?GETDATA@TASKCOLLECTION, ?SETDATA@TASKCOLLECTION, CLRMGR* palette functions.

## Screenshot 21-43-34

- **Module:** TB80UTL
- **Address:** 3947:0174
- **Function:** ?SETDATA@TASKCOLLECTION@@RECHPEX@Z
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** ?SETDATA@TASKCOLLECTION@@RECHPEX@Z
- **Notes:** C++ task collection data setter. Same task collection family.

## Screenshot 21-43-47

- **Module:** TB80UTL
- **Address:** 39FF:001C
- **Function:** PLUGINSVCINIT
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** PLUGINSVCINIT
- **Notes:** Plugin service init. Subtracts 0056 from SP. Functions window shows PLUGINSETLAUNCHBOOK, PLUGINSETTBFRAMEWND, PLUGINSVCINIT, PLUGINSVCSHUTDOWN, PROCESSVALIDF1.

## Screenshot 21-43-57

- **Module:** TB80UTL
- **Address:** 3A3F:0000
- **Function:** LOADRESSTR
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** LOADRESSTR
- **Notes:** Resource string loader. Subtracts 0010 from SP. Functions window shows GETTBKINIPROFILEINT, GHEAPALLOC, GHEAPCREATE, GHEAPDELETE, GHEAPFREE, INITMETRICS, ISPLUGININSTANCE, LOADRESSTR.

## Screenshot 21-44-07

- **Module:** TB80UTL
- **Address:** 367F:02D0
- **Function:** CXTHELPINIT
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** CXTHELPINIT
- **Notes:** Context help init. Moves word ptr 17F0 into AX. Functions window shows CLRMGR*, CXTHELPDLG, CXTHELPEXIT, CXTHELPGETCONTEXT, CXTHELPINIT, CXTHELPSETCONTEXT.

## Screenshot 21-44-22

- **Module:** TB80UTL
- **Address:** 5BA7:0160
- **Function:** GETTBKINIPROFILEINT
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GETTBKINIPROFILEINT
- **Notes:** TBK.INI profile integer read. Calls near ptr 0000. Functions window shows FILEINWINPATH, FILEREQUIRESPLUGINAPI, GDIATAN2, GDIELLIPSEPOINTFROMANGLE, GETASYMINIPROFILEINT, GETCHARINFO.

## Screenshot 21-44-30

- **Module:** TB80UTL
- **Address:** 5BA7:0102
- **Function:** GETTBKINIPROFILESTRING
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GETTBKINIPROFILESTRING
- **Notes:** TBK.INI profile string read. Calls near ptr 0000.

## Screenshot 21-44-37

- **Module:** TB80UTL
- **Address:** 3B6F:0000
- **Function:** INITMETRICS
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** INITMETRICS
- **Notes:** Metrics init. Calls near ptr SETCONVERSIONDC. Functions window shows GETTBKINIPROFILEINT, GHEAPALLOC, INITMETRICS, ISPLUGININSTANCE, LOADRESSTR, ORIENTRECT, PAGETOCLIENT.

## Screenshot 21-44-46

- **Module:** TB80UTL
- **Address:** 3B6F:00FE
- **Function:** SETCONVERSIONDC
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** SETCONVERSIONDC
- **Notes:** Sets conversion DC. Subtracts 0002 from SP. Functions window shows PLUGINSETLAUNCHBOOK, PLUGINSVCINIT, PROCESSVALIDF1, PTONLINE, PXTTOCXT, QUICKSORT, RESTORENDIMETRICS, SETCONVERSIONDC.

## Screenshot 21-44-56

- **Module:** TB80UTL
- **Address:** 3B8F:00A2
- **Function:** CXTTOPXT
- **Prolog:** `mov ax,0D37` / `push ds` / `mov ds,ax`
- **Break on:** CXTTOPXT
- **Notes:** Context to page coordinate conversion. Compares byte ptr 0028. Functions window shows CLRMGR*, CXTHELP*, CXTTOPXT, DEFHELPHOOK, FILEINWINPATH.

## Screenshot 21-45-07

- **Module:** TB80UTL
- **Address:** 3AD7:0000
- **Function:** GHEAPCREATE
- **Prolog:** `mov ax,ds` / `nop` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GHEAPCREATE
- **Notes:** Global heap create. Subtracts 0002 from SP. Functions window shows GHEAPALLOC, GHEAPCREATE, GHEAPDELETE, GHEAPFREE, INITMETRICS.

## Screenshot 21-45-12

- **Module:** TB80UTL
- **Address:** 3AD7:00BE
- **Function:** GHEAPALLOC
- **Prolog:** `mov ax,ds` / `nop` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** GHEAPALLOC
- **Notes:** Global heap alloc. Subtracts 0002 from SP.

## Screenshot 21-45-29

- **Module:** TB80UTL
- **Address:** 3AC7:0624
- **Function:** SYMLOOKUPNUMBER
- **Prolog:** `mov ax,0D37` / `inc bp` / `push bp` / `mov bp,sp`
- **Break on:** SYMLOOKUPDATA
- **Notes:** Symbol table number lookup. Compares word ptr 0A[bp]. Functions window shows SETCONVERSIONDC, SETPLUGINDATA, SORTSTRINGPTRLIST, SYMAPPENDTABLE, SYMCREATETABLE, SYMLOOKUPNUMBER, SYMREMOVETABLE.

---

## Remaining screenshots

The remaining 38 screenshots (21-45-35 through 21-57-37) continue the same pattern: individual function hits in TB80UTL after INITTASK. Functions covered include heap operations, symbol table, plugin services, coordinate conversion, and profile reads. None of these are on the book-open or record-reader path. UTL is the utility and type-table module.

---

## Summary

UTL after INITTASK is a utility initialization pass. It sets up:

- Character and string management
- Task collection (C++ objects)
- Plugin services
- Resource string loading
- Context help
- TBK.INI profile reads
- Metrics and conversion DC
- Global heap
- Symbol table

These are supporting services. The record reader is not here.
