# Trace review — tbwp0026

> Trail, 2026-10-16. Chapter 12. Three traces, no reader. If this sheet and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-16

## What the traces show

### W16 (11 screenshots)

Platform detection, OLE init, and the 32-bit thunk layer. Functions hit:

- GETPLATFORMREF, IS32BITENV
- GETRUNTIMELOCALIZEDDLL
- ACXINITIALIZETOOLBOOKSUPPORT, ACXOLEINITIALIZE
- ASYM_STRINGFROMCLSID
- SETTHUNKINGLAYERSERRORFUNC
- LOADLIBRARYEX32W, GETPROCADDRESS32W

W16 is the command bus. These set up the 32-bit bridge. No book open, no record walk.

### UTL (53 screenshots)

Post-INITTASK utilities. Functions hit:

- GETCHARINFO, GETSTRMGRSTRING
- Task collection getters/setters (C++ objects)
- PLUGINSVCINIT, LOADRESSTR
- CXTHELPINIT, GETTBKINIPROFILEINT/STRING
- INITMETRICS, SETCONVERSIONDC, CXTTOPXT
- GHEAPCREATE, GHEAPALLOC
- SYMLOOKUPNUMBER

UTL holds the object type table and utility services. No record reader.

### BAS (173 screenshots)

Value construction, file open, stack, and chunk handling. Functions hit:

- VALUETOSTRING, VALUENEWSTACK, VALUENEW* family (VALUENEWLONG is a value constructor)
- OBJFILEOPEN (large frame, 0x25A)
- STACKGETSIZE, STACKPUSH
- CDBCHUNKLAST, CDBCHUNKFIND, CDBCHUNKEND
- RESMGR* (resource manager)

## Record reader status

**Not present in these traces.**

- No function reads a far pointer and compares the first word to 0x14.
- No literal `14 00 00` in the stepped code.
- CDBCHUNK* are text/separator walkers (comma, CR/LF, quote). They are not binary record readers.
- OBJFILEOPEN is the file open path. It is downstream of the record reader.
- VALUENEWLONG builds a long value. It is not a record parser.

## Where the reader is

Still unnamed. Prior notes (`tbwp0018/record-reader-candidates.md`) already established:

- No function in the decompiled BAS or RTM regions reads a far pointer and compares to 0x14.
- FUN_10b0_00a6 dispatches on type codes including 0x14. It is a type dispatcher, not a reader.
- The reader is in BAS, but it does not call CDBSENDCREATE (author-only).
- Live tracing after CDBFILEOPEN is the remaining path.

## Significance

These traces confirm the supporting layers:

- W16 sets up the 32-bit thunk and OLE.
- UTL sets up utilities, heap, and the symbol table.
- BAS sets up value constructors, the file open path, and chunk walkers.

They do not advance the record reader search. The 14 00 00 parser is still in an unstepped region of BAS. The next live break is still after CDBFILEOPEN, before the page walk.
