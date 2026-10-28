# TB80BAS — WDW Full Pass 02

> Trail, 2026-10-16. Chapter 12. 173 BAS shots. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-15  
**Source:** BAS - Full Pass 02.zip (173 screenshots across Rar11–Rar19)  
**Debugger:** Open Watcom Debugger on Win98  

This is a full pass through TB80BAS after load. The screenshots step through value constructors, file open, stack operations, chunk handling, and resource management. VALUENEWLONG is among the functions hit.

---

## Rar16 (23 screenshots, 19-55-16 to 19-58-43)

### Screenshot 19-55-16

- **Module:** TB80BAS
- **Address:** 44CF:0DE8
- **Function:** VALUETOSTRING
- **Prolog:** `mov ax,2977` / `push bp` / `mov bp,sp`
- **Break on:** VALUETOSTRING
- **Notes:** Value to string conversion. Pushes multiple word ptr [bp] arguments. Functions window shows VALUENEW* family (VALUENEWLITDBL, VALUENEWLITSTR, VALUENEWLONG, VALUENEWPOINT, VALUENEWRECT, VALUENEWRESOURCE highlighted, VALUENEWSTACK, VALUENEWSTRING, VALUENEWSTRINGEX, VALUENEWTIME).

### Screenshot 19-55-35

- **Module:** TB80BAS
- **Address:** 4867:177C
- **Function:** OBJFILEOPEN
- **Prolog:** `mov ax,2977` / `enter 025A,00`
- **Break on:** OBJFILEOPEN
- **Notes:** Object file open. Large frame (0x25A). Reads word ptr -04[bp], -02[bp]. Functions window shows IMBLACKOUTBMP, IMDRAW, LIONELDEREFBOOK, LOCALANDHELPHOOK, LOOKUPSTDPROPBYNAME, OBJARENACHECK, OBJFILECLOSE, OBJFILECOPY, OBJFILEOPEN, OBJFREE.

### Screenshot 19-55-45

- **Module:** TB80BAS
- **Address:** 451F:0738
- **Function:** STACKGETSIZE
- **Prolog:** `mov ax,2977` / `enter 000A,00`
- **Break on:** STACKGETSIZE
- **Notes:** Stack size query. Compares word ptr 06[bp] and 08[bp]. Functions window shows RESMGRGETREFCNT, RESMGRIMPORT, RESMGROPENBOOK, RESMGRQUERYINFO, RESMGRREPLACE, RESMGRSENDMESSAGE, STACKFREE, STACKGETSIZE, STACKPOP, STACKPUSH.

### Screenshot 19-55-57

- **Module:** TB80BAS
- **Address:** 451F:0000
- **Function:** VALUENEWSTACK
- **Prolog:** `mov ax,2977` / `enter 0044,00`
- **Break on:** VALUENEWSTACK
- **Notes:** New stack value constructor. Loads ES from 0C[bx], pushes word ptr ES:06[bx], ES:04[bx], ES:0C[bx]. Functions window shows VALUENEW* family with VALUENEWRESOURCE highlighted.

### Screenshot 19-56-06

- **Module:** TB80BAS
- **Address:** 451F:0778
- **Function:** STACKPUSH
- **Prolog:** `mov ax,2977` / `enter 001A,00`
- **Break on:** STACKPUSH
- **Notes:** Stack push. Reads byte ptr 09[bp], shifts, compares AX against 0015. Functions window shows RESMGR*, STACKFREE, STACKGETSIZE, STACKPOP, STACKPUSH, STACKPUSHONE, STACKSETELEMENT.

### Screenshot 19-56-22

- **Module:** TB80BAS
- **Address:** 458F:0334
- **Function:** CDBCHUNKLAST
- **Prolog:** `mov ax,2977` / `enter 0010,00`
- **Break on:** CDBCHUNKLAST
- **Notes:** Chunk last. XORs AX, reads word ptr -04[bp], -06[bp], compares word ptr 0A[bp]. Functions window shows ?STACKVALUETOVARIANT, ?STRINGVALUETOVARIANT, ?VALUETOVARIANT, ?VARIANTTARGETSTOOLBOOKARGS, CDBCHUNKEND, CDBCHUNKFIND, CDBCHUNKLAST, CDBCLASSTABLEGETBEHAVIOR, CDBCLEARBOOKREFS, CDBCLIENTSTATUS, CDBCLONEINSTANCE.

---

## Remaining Rar folders

The remaining folders (Rar11, Rar12, Rar13, Rar14, Rar15, Rar17, Rar18, Rar19) continue the same pattern: individual function hits in TB80BAS. Functions covered include:

- Value constructors (VALUENEWLONG, VALUENEWSTRING, VALUENEWPOINT, VALUENEWRECT, VALUENEWRESOURCE, VALUENEWSTACK, VALUENEWTIME)
- File operations (OBJFILEOPEN, OBJFILECLOSE, OBJFILECOPY)
- Stack operations (STACKPUSH, STACKPOP, STACKGETSIZE, STACKFREE)
- Chunk operations (CDBCHUNKLAST, CDBCHUNKFIND, CDBCHUNKEND)
- Resource manager (RESMGRSENDMESSAGE, RESMGRQUERYINFO, RESMGROPENBOOK)
- Object management (OBJFREE, OBJFREENEAR, OBJFREESEG)

VALUENEWLONG is among the value constructors hit. These are the runtime value and object management functions. The record reader is still upstream of these.

---

## Summary

BAS Full Pass 02 covers value construction, file open, stack management, and chunk handling. VALUENEWLONG and the rest of the VALUENEW* family are value constructors. OBJFILEOPEN is the file open path. CDBCHUNK* functions walk chunk structures. None of these is the 14 00 00 record reader. The reader is still unnamed and is not among the functions stepped in this pass.
