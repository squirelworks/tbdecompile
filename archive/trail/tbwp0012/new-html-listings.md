# New HTML Listings — TBCBT, TBDB3, TBDLG, Tbload, TBWIN

> Trail, 2026-10-16. Chapter 17. TBCBT, TBDB3, TBDLG, tbload, TBWIN surveyed. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: attached Ghidra HTML exports

## Tbload.exe (32-bit PE)

- Searches for the string `ZZZTBKBOOKLOC` (data at 0040c61c).
- The search sits in `FUN_00405460` which calls `FUN_00405420` then continues into object setup (`FUN_00405480`, `FUN_004054b0`, `FUN_00405500`).
- This matches the known opener path: locate the magic marker, then hand the book to the engine.
- No direct `JBO` / `03 4A 42 4F` string hit in the truncated search; the signature check is likely a binary compare after the marker is found.

## TBWIN.DLL

- Exports / calls `INIT_TBKWIN`.
- Contains the string `TBKDLLPOPMENU` and `ToolBook`.
- Window-system support, not the book-format parser.

## TBDLG.DLL

- Dialog helpers (`DialogInit`, `GETDLGCTRLID`, `GETDLGITEM`, `SETDLGITEMTEXT`, etc.).
- Standard UI dialog layer.

## TBCBT.DLL

- CBT (computer-based training) support module.
- No strong book/page string surface in the quick scan.

## TBDB3.DLL

- dBASE / database layer (copyright 1990-1995 Asymetrix).
- Not on the NIDA course open path.

## Relevance to open gaps

- Tbload is the only one of these that touches the book marker. The `14 00 00` record reader is still downstream of this (in BAS / RTM after the book is handed over).
- The others are supporting DLLs (windows, dialogs, CBT, database) and can be set aside for the NIDA courseware goal.

Next useful cut on Tbload: walk from the `ZZZTBKBOOKLOC` hit to the first call that crosses into the 16-bit engine (TB80RTM / TB80BAS ordinal).
