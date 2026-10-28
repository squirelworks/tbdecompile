**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# 148-case Switch at 1008:2dc7

> Trail, 2026-10-16. Kept. Chapters 6 and 14. Math, not the reader. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: TB80BAS.DLL.html, segment 1008 (Code2)

## Location

```
Code2:1008:2dc7 ff25  JMP word ptr [DI]
```

Ghidra marks it `FWD[148]`. The jump table lives in the data segment:

```
MOV DI, 0x1d7e
ADD DI, CX
JMP word ptr [DI]
```

CX is the dispatch key. All sampled case targets stay inside segment 1008.

## Containing function

**FUN_1008_2d31** (1008:2d31). Callers: 1008:2cbe, 1008:2cee.

The function is FPU-heavy:
- `FCLEX`
- `FST` / `FSTSW`
- `INT 0x3d` (coprocessor exception check)
- Tests the status word bit 0x8
- `FLD double ptr [BP+6]` / `FSTP` into data-segment doubles

## Pre-switch check

Immediately before the table setup:

```
CMP word ptr [BX], 0x6f6c      ; "lo"
CMP byte ptr [BX+2], 0x67      ; "g"
CMP AL, 0x2
; if all match, set byte at 1630:1d95 = 1
```

This is a special case for the string `"log"`.

## Interpretation

The switch is a **math / transcendental function dispatcher** inside an FPU support routine. The 148 cases stay in segment 1008 and do not call out to the polygon painter (1408) or the object-create path (12c8). It is not the 14 00 00 record reader and not the type dispatcher that reaches PaintPolygon.

## Relation to earlier notes

Segment 1008 also contains `ScaleTwipsToScreen` (FUN_1008_01dd at offset 0x1DD). The switch at 0x2dc7 is in the same large segment but is a separate function (FUN_1008_2d31) concerned with floating-point math, not with bounds scaling or object painting.

## Deeper look (2026-10-14)

The switch entry is `FUN_1008_2d31`. It begins with:

```
MOV AL, byte ptr [BP + -0x11]
OR  AL, AL
JG  LAB_1008_2d71
FCLEX
WAIT
FST double ptr [DAT_1630_1bc0]
FSTSW word ptr [BP + -0xa]
INT 0x3d
TEST word ptr [BP + -0xa], 0x8
```

`FCLEX` / `FST` / `FSTSW` is FPU exception setup. Sampled cases do multiplies and one DOS3CALL. None call into segment 1408 (PaintPolygon) or 12c8 (CDBSENDCREATE).

## Status

Not the page-object or paint path. Not needed for the current book open/render goal.

Filed for later. The 148-case FPU/math dispatcher and the `"log"` special case are documented here so they are available when transcendental or expression evaluation becomes relevant.
