# What the Supporting Modules Actually Contain

> Trail, 2026-10-16. Chapter 17. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: TB80F32L, TB80FLT, TB80JPG, TB80LNL, TB80NET, TB80OCX, TB80RUN, TB80UTL-2, TB80W16, TB80W32, zlib1

## Not stuck on the record reader

The 14 00 00 reader is one open question. These modules are not where it lives. They are the rest of the runtime: media, ActiveX, launch, and UI helpers. Here is what each one actually does.

## Module contents

### TB80LNL.DLL — Multimedia ToolBook Media Engine
- ASYMTBKFX* family: BitBlt, set destination, async, notify, status, destroy.
- MCI: MCISENDCOMMAND, MCISENDSTRING, MCIGETDEVICEID, MCIGETERRORSTRING, yield proc.
- Wave: WAVEINADDBUFFER, WAVEINCLOSE, WAVEINGETDEVCAPS, WAVEINGETNUMDEVS.
- MMIO: MMIOOPEN, MMIOREAD, MMIODESCEND, MMIOCLOSE.
- TIMEGETTIME.

This is the audio/video/MCI path. NIDA lessons that play clips or use MCI go through here.

### TB80W16.DLL — 16-bit thunk + script-editor commands
- DoCmd* surface: DoCmdDraw, DoCmdMouseDown, DoCmdMouseDoubleClick, DoCmdLoad, DoCmdILoad, DoCmdIUnload, DoCmdGoAuthor, DoCmdOcxLoadPicture, DoCmdOleObjectInit, DoCmdCallInstalledMethod, DoCmdGetPropertyArrayValue, DoCmdFreezeEvents, DoCmdMove, DoCmdPasteInit.
- ACTIONGETHANDLER / ACTIONGETSTAGE.

This is the command bus the editor and the runtime use to talk to objects. DoCmdDraw is the nearest thing to a paint entry from the script side.

### TB80OCX.DLL — TBX OLE2 Container Control
- OCXINIT, OCXOLEINITIALIZE / UNINITIALIZE.
- OCXLOADPICTURE / OCXLOADPICTUREVARIANT.
- OCXGETDATAOBJECT / OCXFREEDATAOBJECT.
- ASYM_CREATEBITMAPFROMOLEICON / ASYM_FREEOLEICON.
- OCXGETGUIDLICENSE.

ActiveX / OLE picture loading. Out of scope for the NIDA books themselves, but it is the path that loads OLE-embedded pictures.

### TB80NET.EXE — Network + ACX bootstrap
- ACXINITIALIZETOOLBOOKSUPPORT / ACXUNINITIALIZETOOLBOOKSUPPORT.
- TBKNET3WNDPROC (the network window class).
- TBKBOOKLOC, TBKINIPROFILEINT / STRING, TBKBREAKTHREAD, TBKCOLOR.

This is the process that TB80RUN spawns. It owns the network class and the ACX init that brings the rest of the runtime up.

### TB80RUN.EXE — 32-bit launcher
- String `TB80NET.EXE` and class `TbkNet3TB80`.
- Calls WinExec / CreateProcess.
- Reads ASYM.INI and walks registry keys (HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, etc.).

Confirms the launch seam: 32-bit RUN starts 16-bit NET with the book on the command line.

### TB80FLT.DLL — Common controls + file helpers
- ASYM_BMPBTN, ASYMSHSLDUALINSLIDERCONTROLPROC (custom controls).
- ASYM_GETLONGFILENAME / SHORT / OPENFILE, ASYM_IS32BITENV, ASYM_CGETCWD, ASYM_CLIPEDOPENCBK.

UI controls and long-filename wrappers. Not page content.

### TB80JPG.DLL — JPEG
- JPEG_CREATE_COMPRESS and the usual IJG-style entry points.
- Picture decode only.

### TB80UTL.DLL — Utilities
- ASYM_GETLONGFILENAME / SHORT / OPENFILE / OPENFILEEX.
- HELP* family (HELPFILENAME, HELPEXIT, HELPDIALOGDLL, HELP32W).
- GETTEMPPATH32W / GETTEMPFILENAME32W.
- IS32BITENV, WINHELP32W.

Filename, temp, and help helpers. The object-type table noted earlier lives in this DLL, but this listing does not re-expose it.

### TB80W32.DLL / TB80F32L.dll — 32-bit thunk layers
- W32 has fatal-error strings.
- F32L is the flat thunk support.
- Neither touches book records.

### zlib1.dll
- Modern PE. From the cour1 menu program, not the ToolBook engine.

## What this gives the NIDA path

- **Media.** If a lesson plays sound or MCI, LNL is the module. The NIDA books themselves do not appear to rely on it for the core page graphics.
- **Command bus.** W16’s DoCmdDraw / DoCmdMouseDown are the script-side entries that eventually reach the BAS painters. Useful if we want to trace a paint from the handler rather than from GDI.
- **Launch.** RUN → NET is the real start path. Already noted; this listing confirms the strings.
- **Pictures.** JPG and OCX are the two picture loaders outside BAS. JPG is for JPEG resources; OCX is for OLE-embedded pictures. The carved BMPs in the course books are the BAS/BMP path, not these.

## Still open

The 14 00 00 reader and the PaintPolygon type table remain inside TB80BAS (or the table it fills at runtime). These modules do not contain them. They do contain the media, ActiveX, and launch pieces that a full playback host eventually needs.
