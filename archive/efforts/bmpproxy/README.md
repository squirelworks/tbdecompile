# TB80BMP proxy

A 16-bit stand-in for `TB80BMP.DLL`. It exports ordinals 1 through 93 and
forwards every one to the real DLL, which you rename to `TB80BMR.DLL`.
Ordinal 3 (`TBKBITMAP`) and ordinal 13 (`TBKGRAPHICFX`) are logged to
`C:\TBK\BMPLOG.TXT` before the call goes through.

## Build

Open Watcom, 16-bit. From a Watcom shell in this folder:

```
build.bat
```

That produces `proxy.dll`.

One thing to check on the first build: open `proxy.map` and confirm the
symbol names. The stubs reference `procs`, `logfn`, `log_ord`, `log_a`,
`log_b`, and call `logbmp`. If Watcom decorated any of them, fix the
`EXTRN` lines in `stubs.asm` to match and rebuild.

## Install

In the ToolBook directory on the VM:

1. Rename the real `TB80BMP.DLL` to `TB80BMR.DLL`.
2. Copy `proxy.dll` in as `TB80BMP.DLL`.

Leave `C:\TBK\` present. The log is created there.

## Read the log

`BMPLOG.TXT` starts with one line:

```
proxy up  real=<handle>  resolved=<n>/93
```

`resolved` should be 93. If it is low, the real DLL did not load or an
ordinal is off. Each bitmap call then adds:

```
ord 3  <param1> <param2>
ord 13 <param1> <param2>
```

Ordinal 3 is `TBKBITMAP`, ordinal 13 is `TBKGRAPHICFX`. The two numbers are
the words passed on the stack. They are the lead on where the picture data
crosses in.

## Restore

Delete the proxy `TB80BMP.DLL` and rename `TB80BMR.DLL` back.
