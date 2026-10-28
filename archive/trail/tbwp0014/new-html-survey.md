**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# New HTML Survey — Supporting Modules

> Trail, 2026-10-16. Superseded. Chapter 17. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: attachments TB80F32L, TB80FLT, TB80JPG, TB80LNL, TB80NET, TB80OCX, TB80RUN, TB80UTL-2, TB80W16, TB80W32, zlib1

## Summary

None of these listings contain `CDBSENDCREATE`, `CDBFILEOPEN`, `ZZZTBKBOOKLOC`, a `14 00 00` reader, or `PaintPolygon`. They are supporting modules, not the book engine.

## Per-module

| Module | Format | Role | Book/graphics relevance |
|--------|--------|------|-------------------------|
| TB80F32L.dll | PE | 32-bit flat thunk / support | None. No book keywords. |
| TB80FLT.DLL | NE | Filter / common controls (ASYM_BMPBTN, sliders) | None. |
| TB80JPG.DLL | NE | JPEG (JPEG_CREATE_COMPRESS etc.) | Picture decode only. Not the page record reader. |
| TB80LNL.DLL | NE | Multimedia ToolBook Media Engine (ASYMTBKFX*) | Media effects. No page objects. |
| TB80NET.EXE | NE | Network + ACX init (ACXINITIALIZETOOLBOOKSUPPORT, TBKNET3WNDPROC, TBKBOOKLOC string) | Startup support. Not the open path. |
| TB80OCX.DLL | NE | TBX OLE2 Container Control | ActiveX. Out of NIDA scope for now. |
| TB80RUN.EXE | PE | 32-bit launcher (WinExec/CreateProcess, string TB80NET.EXE) | Confirms the spawn seam. Does not open the book itself. |
| TB80UTL.DLL-2 | NE | Utilities (filename helpers, help) | Same as prior UTL survey. Object-type table already noted elsewhere. |
| TB80W16.DLL | NE | 16-bit thunk / script-editor commands (DoCmd*, ACTIONGETHANDLER) | Already known as thunk layer. |
| TB80W32.DLL | PE | 32-bit thunk layer | Supporting. |
| zlib1.dll | PE (modern) | Compression | From the cour1 menu program, not ToolBook. |

## Takeaway for the NIDA path

The record reader and the type-dispatcher table are still inside TB80BAS (or the runtime-built table it fills). These modules do not move that search.

TB80RUN confirms the intended launch path (32-bit spawn of TB80NET with the book on the command line), which was already noted.

## Status

Supporting-module survey only. No new leads on the 14 00 00 reader or the PaintPolygon type table.
