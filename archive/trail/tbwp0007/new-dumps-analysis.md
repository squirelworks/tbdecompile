# New dump analysis (2026-10-14)

> Trail, 2026-10-16. Chapters 7 and 12. A dump is real only when it contains known book strings. If this sheet and `TBdecompile/record/` disagree, the record wins.

Six additional decompiles arrived. Summary and recommended next actions.

## File inventory

| File | Format | What it is | NIDA relevance |
|------|--------|------------|----------------|
| `decrypt.exe.html` | NE | Compiled ToolBook application. Contains the OPTLOADER expander (`FUN_1000_0031`). Entry 0002:15a4. | Low. Pattern already known. |
| `Inst80.exe.html` | PE (32-bit) | Installer. References `TB80NET.EXE`, `INST80.sbk`, `ASYM.INI`, registry keys, class `TbkNet3TB80`. | Medium. Load-order and registration path. |
| `TB80ATH.EXE.html` | NE | Author executable. ASYMCTL* controls, ASYMSPELL* spell-check, file dialogs (`GETOPENFILENAME`, `GETSAVEFILENAME`). | Low for playback. Authorship milestone. |
| `TB80BAS.DLL-2.html` | NE | Second BAS dump (Asymetrix 1990-1995). | Cross-check only. |
| `TB80UTL.DLL.html` | NE | Utility layer. `ASYM_GETOPENFILENAME`, `ASYM_OPENFILE`, `ASYM_GETSHORTFILENAME`, `IS32BITENV`. | Already known. Object classification table lives here. |
| `TBCBT.DLL.html` / `TBCBT.DLL2.html` | NE | CBT utilities. Printing (`STARTDOC`, `PRINTDLG`, `GETDEVICECAPS`), ASYM_ file helpers. | Low. Printing not required for NIDA lessons. |

## High-value observations

- **Inst80** is the most useful of the set for the current goal. It shows the 32-bit side launching `TB80NET.EXE` and registering system books (`INST80.sbk`). The load sequence host (`nehost/loadseq.py`) already tracks SoftICE order; Inst80 is the installer that prepares that order.
- **decrypt.exe** reuses the same OPTLOADER expander seen in the TB80* DLLs. No new format insight.
- **TB80ATH** confirms the authorship surface (file dialogs, spell-check, controls). Park until the NIDA playback path is solid.
- **TBCBT** is print-oriented. Useful only if a lesson explicitly prints; NIDA courseware does not appear to require it for normal operation.

## Recommended next steps (NIDA-first)

1. **Inst80 load path** — Extract the strings and call sites that launch `TB80NET.EXE` and open `INST80.sbk`. Compare against the existing SoftICE load sequence. File: `tbworkingpapers/tbwp0007/inst80-load.md`.
2. **System book registration** — Confirm whether `INST80.sbk` is a required system book for NIDA or only an installer helper. Cross-check with `toolbook.lst` and the known Nida books (`nc81base.sbk` etc.).
3. **TB80ATH parked** — Note the authorship entry points (file open/save, spell-check) in a one-page bookmark so the path is not lost. Do not dive until NIDA playback is complete.
4. **No action on decrypt.exe or TBCBT** unless a specific NIDA lesson fails in a way that points at them.

## Open minor paths (from prior BAS work)

All previously listed minor paths are resolved. Remaining work is larger functions or the Inst80/TB80ATH surfaces above.
