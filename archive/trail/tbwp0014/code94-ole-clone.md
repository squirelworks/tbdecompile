# Code94 (12e8:0000) — OLE object clone/copy

> Trail, 2026-10-16. Chapter 4. 12e8:0000 is an OLE clone. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What it is

`UndefinedFunction_12e8:0000` is the start of the Code94 region that was previously a large `??` run. Ghidra decompiled it after the region was forced.

The function:

- Takes source and destination object pointers (`param_2`, `param_3`, `param_4`)
- Allocates temporary buffers with `GLOBALLOCK` / `FUN_10d0_1d74`
- Walks a list of sub-objects (`uStack_5a` count, 0xD-byte records)
- Calls `OBJGETFILE`, `OBJOPTOOH`, `OBJLOCK`, `OBJUNLOCK`, `OBJFREESEG`, `OBJTOUCH`
- Invokes OLE dispatch through `CTbkSimpleOLEDispatch_CallMethod` and `CTbkSimpleOLEDispatch_GetProperty`
- Handles BSTR cleanup (`DeleteBSTR`)
- On failure, calls `TOOLBOOKFATAL` with `"Invalid Next ID in Res Seg"`

## What it is not

It is not the book-open path. It is not the 14 00 00 reader. It is OLE automation support for cloning or copying objects that have COM interfaces (ActiveX controls, or objects that expose methods/properties through `IDispatch`).

The string `CTbkSimpleOLEDispatch` appears in several places in the BAS image. This function is one consumer.

## Status

Resolved as OLE object-copy support. Not on the NIDA playback path. The `??` region it came from is real code; this particular function is not the record reader.
