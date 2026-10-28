# What Instructor115 has open

17 October 2026. Source: `Instructor115.dmp`, a Windows minidump, 49,552,800 bytes. The process is `Instructor115.exe` on Windows XP SP3. When this sheet and `TBdecompile/record/` disagree, the record wins.

The process opened the 8.1 lesson with its own 32-bit DLLs. `TB80BAS` and `TB80RTM` are not loaded. The reader in this process is `TB115BAS.DLL`.

File-handle names in the dump are blank. A book is listed below when the process names it as an open book, or when it is on the command line. A module is listed when it is in the module list.

## Books

| Path | How it is named |
|---|---|
| `C:\courses\9e954d01.tbk` | Command line, window title `ToolBook - 9e954d01.tbk`, and `Book "C:\courses\9e954d01.tbk"` |
| `C:\courses\nc81base.sbk` | `Book "C:\courses\nc81base.sbk"` |
| `C:\courses\tb80r.sbk` | `Book "C:\courses\tb80r.sbk"` |
| `C:\courses\tb80anm.sbk` | `Book "C:\courses\tb80anm.sbk"`. A script in it failed to compile. |
| `C:\Program Files\ToolBook\ToolBook 11.5\Instructor.sbk` | Command line, startup system book |

The command line is `Instructor115.exe` with `C:\courses\9e954d01.tbk`, and `SYS:STARTUPSYSBOOK` set to `Instructor.sbk`.

The old system books still name `tb80r.sbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, `nc81trnr.sbk`, and the registry key `App Paths\TB80.EXE`. That is why the old `.sbk` files are required. The lesson asks for them by those file names.

## Modules loaded

All of these are under `C:\Program Files\Common Files\ToolBook\TBSystem\`. `TB115BAS.DLL` is a 32-bit PE (`IMAGE_FILE_MACHINE_I386`). Its image base in this dump is `0x15E0000` and its image size is `0x186000`.

| Module | Image size |
|---|---|
| `TB115ATH.DLL` | `0x2C5000` |
| `TB115RCR.DLL` | `0x2C000` |
| `TB115LNL.DLL` | `0x2F000` |
| `TB115UTL.DLL` | `0x48000` |
| `TB115BMP.DLL` | `0x23000` |
| `TB115OLE.DLL` | `0x18000` |
| `TB115ACX.dll` | `0x3C000` |
| `TB115FLT.DLL` | `0x2E000` |
| `TB115BAS.DLL` | `0x186000` |
| `TB115RCA.DLL` | `0x57000` |
| `TB115CBT.DLL` | `0x11000` |
| `TB115DLG.DLL` | `0x11000` |
| `TB115WIN.DLL` | `0x15000` |
| `TB115REG.DLL` | `0xB000` |
| `TB115NET.DLL` | `0x18000` |
| `TB115ENU1.DLL` | `0xFB000` |
| `TB115ENU2.DLL` | `0x17E000` |
| `TB115CMP.DLL` | `0x80000` |

`Instructor115.exe` itself is at `0x400000`, image size `0x1C8000`.

## Looked up, not the reader

These paths occur as NT object names. They are not in the module list.

| Path |
|---|
| `C:\courses\TB80MAIN.EXE` |
| `C:\courses\TB80RUN.EXE` |
| `C:\courses\Tbload.exe` |
| `C:\courses\TBFILE32.DLL` |
| `Z:\courses\TB80RUN.EXE` |
| `C:\Program Files\Common Files\click2learn\TBSystem\TB80MAIN.EXE` |

`wow32.dll` and `ntvdm.exe` are mapped. That is a 16-bit launch path. It is not the code that has the lesson open.
