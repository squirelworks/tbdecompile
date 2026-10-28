**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# New HTML Listings Survey (nc81int, nc81rec, TB80BMP, TB80ACX, ENU1/2)

> Trail, 2026-10-16. Superseded. Chapter 17. Survey. Author-path readings superseded. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: `/workspace/attachments/*.html` (the newly attached set)

## Summary

None of the newly attached HTML listings contain the 14 00 00 record reader, ZZZTBKBOOKLOC, or CDBSENDCREATE. They are supporting modules.

| File | Role | Book/object relevance |
|------|------|-----------------------|
| nc81int.dll.html | Nida trainer hardware interface (130E, TD2000, 5050, 205E). Exports Int* voltage/switch/fault/card calls. | None. No page or object parsing. |
| nc81rec.dll.html | Session recording. Exports RecStartSession, RecCloseSession, RecBookmarkSession, RecWriteResponse, RecReadVariable, etc. | Session file I/O only. No book format. |
| TB80BMP.DLL.html | Bitmap and GDI helpers (GRAPHIC, BITMAP, DIB, Lz77-style expand). | Graphics painting support. Not the record-to-object path. |
| TB80ACX.DLL.html | ActiveX/OCX stub layer. | No book open or object create. |
| TB80ENU1.DLL.html / TB80ENU2.DLL.html | Language/string resources (NE and PE respectively). | Resource tables only. |
| libgcc_s_seh-1.dll.html | Modern MinGW runtime. | Irrelevant to ToolBook. |

## Implication for the open question

The 14 00 00 record reader remains downstream of Tbload. It is not in these supporting DLLs. Prior notes already placed it in BAS/RTM after the book is handed over (CDBSENDCREATE → FUN_12c8_0850 → bounds write at object+0xf). These new listings do not move that needle.

Next research stays on the BAS create path and the RTM book-open path that feeds it.
